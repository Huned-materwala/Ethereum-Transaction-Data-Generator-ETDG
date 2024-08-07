import os
import pandas as pd
from pathlib import Path

# Function to process each Excel file
def process_excel_file(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)

    # Convert addresses to lowercase and remove leading/trailing whitespace
    df['Addresses'] = df['Addresses'].str.lower().str.strip()

    # Drop rows with missing or non-string values
    df = df.dropna(subset=['Addresses'])
    df = df[df['Addresses'].apply(lambda x: isinstance(x, str))]

    # Remove duplicates
    df = df.drop_duplicates(subset=['Addresses'])

    # Remove addresses that don't start with '0x'
    df = df[df['Addresses'].str.startswith('0x')]

    # Get the addresses as a list
    addresses_list = df['Addresses'].tolist()

    return addresses_list 


# Function to process all Excel files in a folder
def process_folder(folder_path):
    all_addresses = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(folder_path, filename)
            addresses_list = process_excel_file(file_path)
            all_addresses.extend(addresses_list)
    return all_addresses


# Specify the folder containing the Excel files
current_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_dir, 'temp')

# Process all files in the folder
all_addresses = process_folder(folder_path)

# Remove duplicates from the final list
unique_addresses = list(set(all_addresses))

# Print the size of the unique list
print("Size of the unique list:", len(unique_addresses))


# Save the list to a text file
output_file = 'ethereum_addresses.txt'
with open(output_file, 'w') as f:
    for address in unique_addresses:
        f.write(address + '\n')

print(f"Unique addresses saved to {output_file}")
