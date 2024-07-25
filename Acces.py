import requests
import pandas as pd

# Define the URL for the POST request
url = "https://your-qtest-url.com/api/v3/endpoint"  # Replace with your qTest endpoint

# Define the Bearer token for authentication
bearer_token = "YOUR_BEARER_TOKEN"  # Replace with your actual token

# Define the headers for the POST request
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

# Read the Excel file from the current directory
input_file = "input_file.xlsx"  # Replace with the name of your Excel file
data = pd.read_excel(input_file)

# Iterate over each row in the Excel sheet and send a POST request for each user
for index, row in data.iterrows():
    payload = {
        "id": row['Id'],
        "lastName": row['Last Name'],
        "firstName": row['First Name'],
        "mailId": row['Mail Id']
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"Request for user {row['Id']} was successful!")
    else:
        print(f"Failed to make the request for user {row['Id']}. Status code: {response.status_code}")
        print("Response data:", response.text)
