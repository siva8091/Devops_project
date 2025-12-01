#!/usr/bin/env python3
import psycopg2
import requests
import concurrent.futures

# ==============================
# 🔧 HARDCODED DB CONFIG
# ==============================
DB_HOST = "your-db-endpoint.rds.amazonaws.com"
DB_NAME = "sonarqube"
DB_USER = "sonar"
DB_PASS = "yourpassword"
DB_PORT = "5432"

# ==============================
# 🔧 HARDCODED SONAR CONFIG
# ==============================
SONAR_URL = "https://your-sonar-url.com"
SONAR_AUTH = ("your-sonar-username", "your-sonar-password")     # BASIC AUTH
# If using token, use: SONAR_AUTH = ("yourtoken", "")

# ==============================
# ⬇ FUNCTION: FETCH USERS FROM DB
# ==============================
def fetch_users_from_db():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER,
        password=DB_PASS, port=DB_PORT
    )
    
    cur = conn.cursor()
    cur.execute("SELECT external_login FROM users WHERE external_login IS NOT NULL;")
    rows = cur.fetchall()
    
    conn.close()
    
    return [row[0] for row in rows]


# ==============================
# ⬇ FUNCTION: CLEAN USER
# ==============================
def clean_user(login):
    print(f"\n==============================")
    print(f"Processing login: {login}")

    # ----------------------------------------------
    # 1️⃣ REMOVE GLOBAL PERMISSIONS
    # ----------------------------------------------
    global_permissions = [
        "admin", "gateadmin", "profileadmin",
        "provisioning", "scan", "applicationcreator",
        "securityhotspotadmin", "user", "codeviewer"
    ]

    for perm in global_permissions:
        requests.post(
            f"{SONAR_URL}/api/permissions/remove_user",
            auth=SONAR_AUTH,
            data={"permission": perm, "login": login}
        )

    print("   ✔ Global permissions removed")

    # ----------------------------------------------
    # 2️⃣ REMOVE PROJECT PERMISSIONS
    # ----------------------------------------------
    proj_res = requests.get(
        f"{SONAR_URL}/api/projects/search",
        auth=SONAR_AUTH
    ).json()

    if "components" in proj_res:
        for project in proj_res["components"]:
            project_key = project["key"]
            requests.post(
                f"{SONAR_URL}/api/permissions/remove_user",
                auth=SONAR_AUTH,
                data={"projectKey": project_key, "login": login}
            )

        print("   ✔ Project permissions removed")

    # ----------------------------------------------
    # 3️⃣ DEACTIVATE USER
    # ----------------------------------------------
    requests.post(
        f"{SONAR_URL}/api/users/deactivate",
        auth=SONAR_AUTH,
        data={"login": login}
    )

    print("   ✔ User deactivated")
    print(f"Completed: {login}")
    print("==============================")


# ==============================
# 🚀 MAIN
# ==============================
def main():
    users = fetch_users_from_db()
    print(f"\nTotal users fetched from DB: {len(users)}")

    # Run cleanup in parallel (10× faster)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(clean_user, users)


if __name__ == "__main__":
    main()
