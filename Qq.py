import requests

# SonarQube instance details
SONARQUBE_URL = "http://your-sonarqube-instance.com"  # Replace with your SonarQube instance URL
SONARQUBE_TOKEN = "your_sonarqube_api_token"  # Replace with your SonarQube API token
QUALITY_GATE_NAME = "your_quality_gate_name"  # Replace with your quality gate name
PERMISSION = "gateadmin"  # The permission to be removed (edit permission for quality gate)

# API headers with authentication
headers = {
    'Authorization': f'Basic {SONARQUBE_TOKEN}',
}

# Step 1: Get list of users who have access to the specified quality gate
def get_users_with_permission(quality_gate_name):
    url = f"{SONARQUBE_URL}/api/permissions/search"
    params = {
        'q': quality_gate_name,
        'permission': PERMISSION,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    users = response.json().get('users', [])
    return users

# Step 2: Remove edit permission for each user
def remove_edit_permission_for_users(users, quality_gate_name):
    url = f"{SONARQUBE_URL}/api/permissions/remove"
    for user in users:
        params = {
            'login': user['login'],  # The user's login name
            'permission': PERMISSION,
            'resource': quality_gate_name,
        }
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        print(f"Removed edit permission for user: {user['login']}")

def main():
    # Get users with edit permission on the quality gate
    users = get_users_with_permission(QUALITY_GATE_NAME)

    if not users:
        print(f"No users found with edit permission for quality gate: {QUALITY_GATE_NAME}")
        return

    # Remove edit permission for all users
    remove_edit_permission_for_users(users, QUALITY_GATE_NAME)

if __name__ == "__main__":
    main()
