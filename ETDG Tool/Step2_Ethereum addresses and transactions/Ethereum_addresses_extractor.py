import requests
import csv

def fetch_block_transactions(block_number, api_key):
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={block_number}&boolean=true&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['result']['transactions']
    else:
        print("Error:", response.status_code)
        return []

def extract_unique_addresses(transactions):
    addresses = set()
    for tx in transactions:
        if 'from' in tx:
            addresses.add(tx['from'])
        if 'to' in tx:
            addresses.add(tx['to'])
    return addresses

def save_addresses_to_csv(addresses, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Addresses'])
        for address in addresses:
            writer.writerow([address])

# Replace 'start_block' and 'end_block' with the range of block numbers you want to query
start_block = 19673900
end_block = 19773900  # Fetching transactions for blocks 100,000 blocks based on API call limit
# Replace 'your_api_key' with your Etherscan API key
api_key = '5C552HMVTTXATA9F2GQT3A663YN8J4GSUN'
# Replace 'output_file.csv' with the desired filename for the CSV file
output_file = 'Ethereum_addresses.csv'

unique_addresses = set()

for block_number in range(start_block, end_block + 1):
    print(block_number, "\n")
    transactions = fetch_block_transactions(hex(block_number), api_key)
    if transactions:
        unique_addresses.update(extract_unique_addresses(transactions))

if unique_addresses:
    save_addresses_to_csv(unique_addresses, output_file)
    print(f"Unique addresses saved to {output_file}")
else:
    print("No transactions found in the specified block range.")