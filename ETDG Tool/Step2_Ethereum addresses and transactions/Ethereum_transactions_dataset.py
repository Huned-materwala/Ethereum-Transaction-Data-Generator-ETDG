import json
import pandas as pd

# Initialize lists to hold parsed JSON objects
data_before_filter = []
data_after_filter = []

# Read the JSON lines from the file and handle potential errors
file_path = './Ethereum transactions_Json/ethereum_transactions_1_10000.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()
    total_lines = len(lines)
    
    for i, line in enumerate(lines):
        try:
            # Convert single quotes to double quotes to make it valid JSON
            json_str = line.strip().replace("'", '"')
            # Parse the modified JSON string as a Python dictionary
            json_obj = json.loads(json_str)
            
            # Append to the initial data list
            data_before_filter.append(json_obj)
            
            # Append to filtered data list if isError is not '1' and value is not '0'
            if json_obj.get('isError') != '1' and json_obj.get('value') != '0':
                data_after_filter.append(json_obj)
                
        except json.JSONDecodeError:
            pass  # Ignore lines that cannot be parsed
        
        # Print progress
        if (i + 1) % max((total_lines // 10), 1) == 0 or (i + 1) == total_lines:
            progress = ((i + 1) / total_lines) * 100
            print(f"Progress: {progress:.2f}%")

# Convert the filtered list of dictionaries to a DataFrame
df = pd.DataFrame(data_after_filter)

# Save the DataFrame to a text file
df.to_csv('./Ethereum transactions_dataset/ethereum_transactions_1_10000.txt', sep='\t', index=False)

# Print the number of transactions before and after filtering
print(f"Number of transactions before filtering: {len(data_before_filter)}")
print(f"Number of transactions after filtering: {len(data_after_filter)}")