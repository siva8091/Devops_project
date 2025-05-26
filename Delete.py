import pandas as pd
import requests

# === CONFIGURATION ===
qtest_domain = 'https://<your-qtest-domain>.qtestnet.com'
project_id = '<your-project-id>'
api_token = '<your-api-token>'  # Bearer token
excel_path = 'module_ids.xlsx'

headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

# === READ MODULE IDS FROM EXCEL ===
df = pd.read_excel(excel_path)
module_ids = df['module_id'].dropna().astype(int).tolist()

# === FUNCTION TO DELETE MODULE ===
def delete_module(module_id):
    url = f'{qtest_domain}/api/v3/projects/{project_id}/modules/{module_id}'
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f'Deleted module ID: {module_id}')
    else:
        print(f'Failed to delete module ID {module_id}: {response.status_code}, {response.text}')

# === MAIN SCRIPT ===
for module_id in module_ids:
    print(f'Processing module ID: {module_id}')
    delete_module(module_id)
