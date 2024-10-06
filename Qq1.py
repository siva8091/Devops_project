import requests

# SonarQube instance details
SONARQUBE_URL = "http://your-sonarqube-instance.com"  # Replace with your SonarQube instance URL
SONARQUBE_TOKEN = "your_sonarqube_api_token"  # Replace with your SonarQube API token
QUALITY_GATE_NAME = "test_sonar"  # Hardcoded quality gate name
PERMISSION = "EDIT"  # Permission we are interested in (Edit permission)

# API headers with authentication
headers = {
    'Authorization': f'Basic {SONARQUBE_TOKEN}',
}

# Step 1: Get list of users with edit permissions for the quality gate (using only gateName)
def get_users_with_edit_permission(quality_gate_name):
    url = f"{SONARQUBE_URL}/api/qualitygates/search_users"
    params = {
        'gateName': quality_gate_name,  # Using only gateName parameter
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('users', [])

# Step 2: Remove edit permission for each user
def remove_edit_permission_for_users(users, quality_gate_name):
    url = f"{SONARQUBE_URL}/api/qualitygates/remove_user"
    for user in users:
        params = {
            'login': user['login'],  # The user's login name
            'gateName': quality_gate_name  # Using gateName parameter
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 204:
            print(f"Removed edit permission for user: {user['login']}")
        else:
            print(f"Failed to remove permission for user: {user['login']} (status code: {response.status_code})")

# Main function to execute the script
def main():
    # Get users with edit permissions on the quality gate
    users = get_users_with_edit_permission(QUALITY_GATE_NAME)
    
    if not users:
        print(f"No users found with edit permission for quality gate: {QUALITY_GATE_NAME}")
        return

    # Remove edit permission for all users
    remove_edit_permission_for_users(users, QUALITY_GATE_NAME)

if __name__ == "__main__":
    main()
