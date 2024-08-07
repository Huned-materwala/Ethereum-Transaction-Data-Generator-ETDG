'''
This python code is used to extract Ethereum transactions per account from Etherscan.io
The accounts addresses are stored in a text file. The code fetches the addresses from the text file.
Then, for each address the transactions are extracted.
The extracted transactions are saved in a text file.
'''

# Importing libraries
import requests

# Defining a function to fetch Ethereum transactions
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

# Read Ethereum addresses from the text file containing addresses
address_file = 'ethereum_addresses.txt'
addresses = []

# Read addresses from the text file
with open(address_file, 'r') as file:
    for line in file:
        address = line.strip()  # Remove leading/trailing whitespace
        addresses.append(address)

# Etherscan API key
api_key = 'N6ZPCGAT8DVMSDDHCBNR6FGTIDR2TGKJGF'

# Fetch transactions for all addresses
all_transactions = []

for address in addresses[235006:270002]:
    transactions = get_eth_transactions(address, api_key)
    if transactions:
        all_transactions.extend(transactions)

# Save transactions to a text file
output_file = 'ethereum_transactions_235006_270002.txt'
with open(output_file, 'w') as file:
    for transaction in all_transactions:
        file.write(str(transaction) + '\n')

print(f"All transactions saved to {output_file}")
