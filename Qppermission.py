import requests
import pandas as pd
import os

# Hardcoded quality gate name
quality_gate_name = 'YourQualityGateName'

# API endpoint
api_url = 'https://your-sonarqube-instance/api/qualitygates/remove_user'

# API authentication (if needed, use a token or username/password)
headers = {
    'Authorization': 'Basic YOUR_API_TOKEN'  # Replace with your authentication method
}

# Read the login list from Excel
def read_logins_from_excel(file_path):
    # Load the Excel sheet into a pandas DataFrame
    df = pd.read_excel(file_path)
    
    # Assuming the login column is named 'login' in the Excel file
    login_list = df['login'].tolist()
    
    return login_list

# Function to remove a user from the quality gate
def remove_user_from_quality_gate(login, quality_gate_name):
    data = {
        'login': login,
        'qualityGate': quality_gate_name  # Assuming this is how the API expects the quality gate
    }
    
    response = requests.post(api_url, headers=headers, data=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Successfully removed user {login} from quality gate {quality_gate_name}")
    else:
        print(f"Failed to remove user {login}. Status code: {response.status_code}")

# Main function to process the list
def main():
    # File path to the Excel sheet in Jenkins workspace
    jenkins_workspace = os.getenv('WORKSPACE')  # Gets the Jenkins workspace path from the environment
    excel_file_path = os.path.join(jenkins_workspace, 'user_logins.xlsx')  # Assuming 'user_logins.xlsx' is in the workspace
    
    # Read the login list from the Excel file
    logins = read_logins_from_excel(excel_file_path)
    
    # Loop through the login list and remove each user
    for login in logins:
        remove_user_from_quality_gate(login, quality_gate_name)

if __name__ == '__main__':
    main()
