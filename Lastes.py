import requests
import json

# Replace these with your actual SonarQube details
SONAR_URL = "https://your-sonarqube-instance.com"
API_TOKEN = "your_api_token"
QUALITY_GATE_NAME = "your_quality_gate_name"
HEADERS = {
    "Authorization": f"Basic {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_quality_gate_id_by_name(quality_gate_name):
    """Get the quality gate ID from its name."""
    url = f"{SONAR_URL}/api/qualitygates/list"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        quality_gates = response.json().get('qualitygates', [])
        for gate in quality_gates:
            if gate['name'] == quality_gate_name:
                return gate['id']
        print(f"Quality gate with name '{quality_gate_name}' not found.")
        return None
    else:
        print(f"Failed to fetch quality gates: {response.status_code}")
        return None

def get_users_with_access_to_quality_gate(quality_gate_id):
    """Get a list of users who have access to the quality gate."""
    url = f"{SONAR_URL}/api/qualitygates/users"
    params = {
        'gateId': quality_gate_id
    }
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        return response.json().get('users', [])
    else:
        print(f"Failed to fetch users for quality gate {quality_gate_id}: {response.status_code}")
        return []

def remove_edit_permission(user_login, quality_gate_id):
    """Remove the edit permission for a user from the selected quality gate."""
    url = f"{SONAR_URL}/api/qualitygates/permissions/remove"
    data = {
        "gateId": quality_gate_id,
        "login": user_login,
        "permission": "edit"
    }
    response = requests.post(url, headers=HEADERS, data=data)
    
    if response.status_code == 204:
        print(f"Successfully removed edit permission for {user_login}")
    else:
        print(f"Failed to remove edit permission for {user_login}: {response.status_code}, {response.text}")

def main():
    # Step 1: Get quality gate ID by its name
    quality_gate_id = get_quality_gate_id_by_name(QUALITY_GATE_NAME)
    
    if quality_gate_id:
        print(f"Quality gate ID for '{QUALITY_GATE_NAME}' is {quality_gate_id}")
        
        # Step 2: Get users who have access to the quality gate
        users = get_users_with_access_to_quality_gate(quality_gate_id)
        
        if users:
            print(f"Users with access to quality gate {QUALITY_GATE_NAME}: {[user['login'] for user in users]}")
            
            # Step 3: Remove edit permission for each user
            for user in users:
                remove_edit_permission(user['login'], quality_gate_id)
        else:
            print("No users found with access to the selected quality gate.")
    else:
        print(f"Unable to find the quality gate with the name '{QUALITY_GATE_NAME}'.")

if __name__ == "__main__":
    main()
