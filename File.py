# Define input and output file paths
input_file = 'input.txt'
output_file = 'output.txt'

# Read the input file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Open the output file to write the transformed lines
with open(output_file, 'w') as file:
    for line in lines:
        # Strip newline characters and add quotes and comma
        file.write(f"'{line.strip()}',\n")

print(f"Transformed data has been written to {output_file}")
