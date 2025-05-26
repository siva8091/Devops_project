import requests
import pandas as pd

# Configuration
qtest_domain = "https://your-qtest-domain.qtestnet.com"
project_id = 12345  # Replace with your qTest project ID
parent_module_id = 67890  # Replace with your parent module ID
api_token = "your-api-token"  # Replace with your qTest API token

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}"
}

# Get list of all modules under a parent module
def get_modules(project_id, parent_id):
    url = f"{qtest_domain}/api/v3/projects/{project_id}/modules?parentId={parent_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        modules = response.json()
        return [module["id"] for module in modules]
    else:
        print(f"Failed to retrieve modules: {response.status_code} {response.text}")
        return []

# Save module IDs to Excel
def save_to_excel(module_ids, filename="module_ids.xlsx"):
    df = pd.DataFrame(module_ids, columns=["Module ID"])
    df.to_excel(filename, index=False)
    print(f"Module IDs saved to {filename}")

# Main logic
if __name__ == "__main__":
    module_ids = get_modules(project_id, parent_module_id)
    if module_ids:
        save_to_excel(module_ids)
    else:
        print("No module IDs found.")
