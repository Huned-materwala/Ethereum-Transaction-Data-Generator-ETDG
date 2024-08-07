# Import libraries
import yaml
import csv

####################################################

# Open YAML file and load the data
with open('scams.yaml', 'r') as file:
    data = yaml.safe_load(file)

####################################################

# Define a function to extract addresses and their corresponding categories
def extract_addresses_and_categories(yaml_data):
    addresses_and_categories = []
    unique_addresses = set()  # Set to store unique addresses
    for entry in yaml_data:
        if 'addresses' in entry:
            addresses = entry['addresses']
            category = entry['category']
            if category == 'Scam':
                category = 'Scamming'  # Replace 'Scam' with 'Scamming'
            for address in addresses:
                address = address.lower()  # Convert address to lowercase
                if address.startswith('0x'):  # Check if address starts with '0x'
                    if address not in unique_addresses:  # Check if address is not already in the set
                        unique_addresses.add(address)  # Add address to set
                        addresses_and_categories.append({'address': address, 'category': category})
    return addresses_and_categories

####################################################

# Extract addresses and categories
addresses_and_categories = extract_addresses_and_categories(data)

####################################################

# Write addresses and categories to a CSV file
with open('malicious_addresses_and_categories.csv', 'w', newline='') as csvfile:
    fieldnames = ['address', 'category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in addresses_and_categories:
        writer.writerow({'address': item['address'], 'category': item['category']})

####################################################

print("Data has been written to addresses_and_categories.csv")