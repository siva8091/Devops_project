import csv
import requests

SONARQUBE_URL = "http://your-sonarqube-instance-url"
SONARQUBE_TOKEN = "your-sonarqube-token"

def remove_gate_admin_role(username):
    url = f"{SONARQUBE_URL}/api/permissions/remove_user_permission"
    headers = {
        "Authorization": f"Bearer {SONARQUBE_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "login": username,
        "permission": "gateadmin"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"Removed gate admin role for {username}")
    else:
        print(f"Failed to remove gate admin role for {username}. Status code: {response.status_code}")

def main():
    with open('user_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            username = row[0]  # Assuming username is in the first column
            remove_gate_admin_role(username)

if __name__ == "__main__":
    main()
