# Import libraries
import csv
import shutil

####################################################

# Load addresses and corresponding fraud categories from 'malicious_addresses_and_categories.csv' file
addresses_with_categories = {}
with open('malicious_addresses_and_categories.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        address = row[0]
        category = row[1]
        addresses_with_categories[address] = category

####################################################

# Make a copy of 'malicious_transactions.csv' file
shutil.copyfile('malicious_transactions.csv', 'malicious_transactions_labeled.csv')

####################################################

# Update 'malicious_transactions_labeled.csv' with 'Fraud' column
with open('malicious_transactions_labeled.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    with open('malicious_transactions_labeled_temp.csv', 'w', newline='') as csvfile_temp:
        writer = csv.writer(csvfile_temp)
        header = next(reader)  # Read the header row
        header.append('Fraud')  # Add 'Fraud' column to header
        writer.writerow(header)  # Write the updated header to the temp file
        for row in reader:
            sender_address = row[6]
            receiver_address = row[7]
            fraud_category = None

            # Skip rows without receiver address
            if receiver_address == '':
                continue

            # Conditions to label the transactions based on fraud categories
            if sender_address in addresses_with_categories and receiver_address not in addresses_with_categories:
                fraud_category = addresses_with_categories[sender_address]
            elif sender_address not in addresses_with_categories and receiver_address in addresses_with_categories:
                fraud_category = addresses_with_categories[receiver_address]
            elif sender_address in addresses_with_categories and receiver_address in addresses_with_categories:
                if  addresses_with_categories[sender_address] ==  addresses_with_categories[receiver_address]:
                    fraud_category = addresses_with_categories[sender_address]
                else:
                    fraud_category = 'multi-category'
            else:
                fraud_category = 'null'

            row.append(fraud_category)
            writer.writerow(row)

# Replace the original csv2 with the temp file
shutil.move('malicious_transactions_labeled_temp.csv', 'malicious_transactions_labeled.csv')
print("Done!")