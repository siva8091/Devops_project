import csv
import requests
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========= CONFIGURATION =========
SONAR_URL = "https://yoursonarurl.com"
USERNAME = "your-username"
PASSWORD = "your-password"
CSV_FILE = "input.csv"
MAX_WORKERS = 20  # Speed multiplier (10–30 is safe)
# =================================

AUTH = (USERNAME, PASSWORD)


# -------------------------------
# GET LOGIN FROM NAME
# -------------------------------
def get_login_from_name(name):
    url = f"{SONAR_URL}/api/users/search"
    params = {"q": name}

    r = requests.get(url, params=params, auth=AUTH)
    if r.status_code != 200:
        print(f"[ERROR] Searching user {name}: {r.text}")
        return None

    users = r.json().get("users", [])
    if not users:
        return None

    for u in users:
        if u.get("name", "").lower() == name.lower():
            return u.get("login")

    return users[0].get("login")


# -------------------------------
# REMOVE ONE GLOBAL PERMISSION
# -------------------------------
def remove_single_global(template_key, perm_key, login):
    url = f"{SONAR_URL}/api/permissions/remove_user"
    params = {
        "templateKey": template_key,
        "login": login,
        "permission": perm_key
    }
    r = requests.post(url, params=params, auth=AUTH)
    return (perm_key, r.status_code)


# -------------------------------
# REMOVE GLOBAL PERMISSIONS (PARALLEL)
# -------------------------------
def remove_global_permissions(login):
    print("   Removing global permissions (parallel)...")

    template_url = f"{SONAR_URL}/api/permissions/search_templates"
    r = requests.get(template_url, auth=AUTH)

    if r.status_code != 200:
        print(f"[ERROR] Fetching templates: {r.text}")
        return

    templates = r.json().get("permissionTemplates", [])
    jobs = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for template in templates:
            key = template.get("key")

            perm_url = f"{SONAR_URL}/api/permissions/search_template_permissions"
            r2 = requests.get(perm_url, params={"templateKey": key}, auth=AUTH)

            if r2.status_code != 200:
                print(f"[ERROR] Template perms for {key}: {r2.text}")
                continue

            perms = r2.json().get("permissions", [])

            for p in perms:
                perm_key = p.get("key")
                jobs.append(
                    executor.submit(remove_single_global, key, perm_key, login)
                )

        # Wait for all tasks
        for future in as_completed(jobs):
            perm, status = future.result()
            if status == 204:
                print(f"      ✔ Removed global permission: {perm}")


# -------------------------------
# REMOVE ONE PROJECT PERMISSION
# -------------------------------
def remove_single_project_permission(project_key, perm, login):
    url = f"{SONAR_URL}/api/permissions/remove_user"
    params = {
        "projectKey": project_key,
        "login": login,
        "permission": perm
    }
    r = requests.post(url, params=params, auth=AUTH)
    return (project_key, perm, r.status_code)


# -------------------------------
# REMOVE PROJECT PERMISSIONS (PARALLEL)
# -------------------------------
def remove_project_permissions(login):
    print("   Removing project permissions (parallel)...")

    page = 1
    permissions = [
        "admin", "issueadmin", "securityhotspotadmin",
        "scan", "codeviewer", "user"
    ]

    jobs = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while True:
            url = f"{SONAR_URL}/api/projects/search"
            params = {"p": page, "ps": 500}

            r = requests.get(url, params=params, auth=AUTH)
            if r.status_code != 200:
                print(f"[ERROR] Fetching projects: {r.text}")
                return

            projects = r.json().get("components", [])
            if not projects:
                break

            # Submit jobs in parallel
            for proj in projects:
                project_key = proj["key"]
                for perm in permissions:
                    jobs.append(
                        executor.submit(remove_single_project_permission,
                                        project_key, perm, login)
                    )

            page += 1

        # Wait for all tasks
        for future in as_completed(jobs):
            project_key, perm, status = future.result()
            if status == 204:
                print(f"      ✔ Removed {perm} from {project_key}")


# -------------------------------
# DEACTIVATE USER
# -------------------------------
def deactivate_user(login):
    print("   Deactivating user...")
    url = f"{SONAR_URL}/api/users/deactivate"
    r = requests.post(url, params={"login": login}, auth=AUTH)

    if r.status_code == 204:
        print("      ✔ User deactivated")
    else:
        print(f"      [INFO] Deactivate skipped: {r.text}")


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def process_users():
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"].strip()
                print("\n==============================")
                print(f"Processing user: {name}")

                login = get_login_from_name(name)
                if not login:
                    print(f"[ERROR] Login not found for {name}")
                    continue

                print(f"   Found login: {login}")

                remove_global_permissions(login)
                remove_project_permissions(login)
                deactivate_user(login)

                print(f"✔ Completed: {name} ({login})")
                print("==============================")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


# Run script
process_users()
