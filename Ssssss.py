#!/usr/bin/env python3
import csv
import psycopg2
import requests
import concurrent.futures

# ================================
# 🔧 DB DETAILS (HARDCODE BELOW)
# ================================
DB_HOST = "your-db-endpoint"
DB_PORT = "5432"
DB_NAME = "sonarqube"
DB_USER = "sonar"
DB_PASS = "yourpassword"

# ================================
# 🔧 SONAR DETAILS
# ================================
SONAR_URL = "https://your-sonar-url.com"
SONAR_AUTH = ("your-sonar-username", "your-sonar-password")

CSV_FILE = "input.csv"   # must contain: external_login


# ================================
# 🔥 GET LOGIN FROM SONAR DB
# ================================
def get_sonar_login(external_login):
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            dbname=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT login 
            FROM public.users 
            WHERE external_login = %s
        """, (external_login,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception as e:
        print(f"[DB ERROR] Cannot fetch login for {external_login}: {e}")
        return None


# ================================
# 🔥 REMOVE PERMISSIONS & DEACTIVATE
# ================================
def clean_user(external_login):
    print(f"\n==============================================")
    print(f"Processing external_login: {external_login}")

    # 1️⃣ DB LOOKUP
    login = get_sonar_login(external_login)

    if not login:
        print(f"❌ No login found for external_login: {external_login}")
        return

    print(f"✔ Found Sonar login in DB: {login}")

    # 2️⃣ REMOVE GLOBAL PERMISSIONS
    global_perms = [
        "admin", "gateadmin", "profileadmin", "provisioning",
        "scan", "applicationcreator", "securityhotspotadmin",
        "user", "codeviewer"
    ]

    for perm in global_perms:
        requests.post(
            f"{SONAR_URL}/api/permissions/remove_user",
            auth=SONAR_AUTH,
            data={"permission": perm, "login": login}
        )
    print("✔ Removed global permissions")

    # 3️⃣ REMOVE PROJECT PERMISSIONS
    proj_list = requests.get(
        f"{SONAR_URL}/api/projects/search",
        auth=SONAR_AUTH
    ).json()

    if "components" in proj_list:
        for proj in proj_list["components"]:
            project_key = proj["key"]
            requests.post(
                f"{SONAR_URL}/api/permissions/remove_user",
                auth=SONAR_AUTH,
                data={"projectKey": project_key, "login": login}
            )
    print("✔ Removed all project permissions")

    # 4️⃣ DEACTIVATE USER
    requests.post(
        f"{SONAR_URL}/api/users/deactivate",
        auth=SONAR_AUTH,
        data={"login": login}
    )
    print("✔ User deactivated")

    print(f"✔ Completed: {external_login} ({login})")
    print("==============================================")


# ================================
# 🚀 MAIN
# ================================
def main():
    external_logins = []

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            external_logins.append(row["external_login"].strip())

    print(f"\nFound {len(external_logins)} users in CSV")

    # Parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(clean_user, external_logins)


if __name__ == "__main__":
    main()
