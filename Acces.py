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

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")
parser.add_argument("--jenkins_base")
parser.add_argument("--token")

args = parser.parse_args()

# ✅ IMPORTANT: override old hardcoded values
INPUT_FILE = args.input
OUTPUT_CSV = args.output
JENKINS_BASE = args.jenkins_base
J_TOKEN = args.token





#####
# --- ARGUMENTS (already correct in your script) ---
parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")
parser.add_argument("--jenkins_base")
parser.add_argument("--token")

args = parser.parse_args()

# --- USE PIPELINE VALUES (FINAL FIX) ---
WORKSPACE = os.environ.get("WORKSPACE", ".")

INPUT_FILE = args.input if args.input else os.path.join(WORKSPACE, "jenkins_jobs.txt")
OUTPUT_CSV = args.output if args.output else os.path.join(WORKSPACE, "output.csv")
PROGRESS_FILE = os.path.join(WORKSPACE, "progress.json")

JENKINS_BASE = args.jenkins_base if args.jenkins_base else JENKINS_BASE
J_TOKEN = args.token if args.token else J_TOKEN

# --- DEBUG (optional, remove later) ---
print("INPUT_FILE:", INPUT_FILE)
print("OUTPUT_CSV:", OUTPUT_CSV)

