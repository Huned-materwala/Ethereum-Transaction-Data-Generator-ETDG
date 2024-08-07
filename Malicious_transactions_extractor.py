'''
This python code is used to extract Ethereum transactions per account from Etherscan.io
The accounts addresses are stored in a text file. The code fetches the addresses from the text file.
Then, for each address the transactions are extracted.
The extracted transactions are saved in a csv file.
'''

# Importing libraries
import requests
import csv

####################################################

# Defining a function to fetch Ethereum transaction
def get_eth_transactions(address, api_key):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':
            return data['result']
        else:
            print(f"Error for address {address}:", data['message'])
            return []
    else:
        print(f"Error for address {address}:", response.status_code)
        return []

####################################################

# Read Ethereum addresses from the CSV file containing malicious addresses
address_file = 'malicious_addresses_and_categories.csv'
addresses = []

####################################################

# Read addresses from the first column of the CSV file
with open(address_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        addresses.append(row[0])

####################################################

# Etherscan API key
api_key = '5C552HMVTTXATA9F2GQT3A663YN8J4GSUN'

####################################################
'''
The code section below saves the transactions extracted from each address in a different CSV file.
The code will fetch transactions for each addresses listed in the address_list.txt file and then
save them to a CSV file named '{address}.csv'.


for address in addresses:
    transactions = get_eth_transactions(address, api_key)
    if transactions:
        csv_file = f"{address}_transactions.csv"
        save_transactions_to_csv(transactions, csv_file)
        print(f"Transactions for {address} saved to {csv_file}")
    else:
        print(f"No transactions found for {address}")

'''

####################################################

'''
The code section below saves the transactions extracted from all the addresses in a single CSV file. 
The code will fetch transactions for all addresses listed in the address_list.txt file,
accumulate them into a single list 'all_transactions', and then save them to a CSV file named 'ethereum_transactions.csv'.
'''

all_transactions = []

for address in addresses:
    transactions = get_eth_transactions(address, api_key)
    if transactions:
        all_transactions.extend(transactions)

# Define CSV headers
if all_transactions:
    headers = all_transactions[0].keys()
    csv_file = 'malicious_transactions.csv'

    # Write all transactions to a single CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for tx in all_transactions:
            writer.writerow(tx)
        print(f"All transactions saved to {csv_file}")
else:
    print("No transactions found for any address.")