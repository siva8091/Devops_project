import json

# Specify the input and output file names
input_file = 'data.json'
output_file = 'output.txt'

# Read the JSON data from the input file
with open(input_file, 'r') as file:
    data = json.load(file)

# Extract the value for the key 'login'
login_value = data.get('login')

# Write the extracted value to the output file
if login_value is not None:
    with open(output_file, 'w') as file:
        file.write(f"login: {login_value}\n")
    print(f"Successfully written to {output_file}: login: {login_value}")
else:
    print("Key 'login' not found in the JSON data.")
