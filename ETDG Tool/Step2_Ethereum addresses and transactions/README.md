# Ethereum addresses and transactions extraction

This step involves the execution of the following stages:

1. Extract Ethereum account addresses
2. Preprocess Ethereum account addresses
3. Extract transactions for Ethereum addresses
4. Convert JSON transaction data into text format:

---

**Extract Ethereum account addresses**
1.	Run the ‘Ethereum_addresses_extractor.py’ code to extract the addresses for Ethereum accounts and save them in a CSV file. The ‘Ethereum_addresses_extractor.py’ code performs the following operations:
    - Defines the function to extract transactions for a block
    - Defines the function to extract addresses for the transactions
    - Defines the function to save addresses to a CSV file

(Note: There are more than 268 million Ethereum addresses as of 8 May 2024. Extracting these addresses would take an enormous amount of time, considering the limit of 100,000 API calls/per day for a free Etherscan account. Consequently, the only finalized last 100,000 blocks as of 1714521873 timestamp (19673900 – 19773900) are queried to extract the addresses involved in transactions within these blocks. 100,000 is selected based on the daily API call limit.)

**Preprocess Ethereum account addresses**
1.	Run the ‘Address_preprocessor_concatenator.py’ code to extract the preprocess and concatenate the addresses stored in the CSV files (obtained from the previous step). The final list of addresses is saved in a text file. Text files are chosen over CSV files to save the data and avoid the Excel limit of 1,048,576 rows. The ‘Address_preprocessor_concatenator.py’ performs the following operations:
    - Defines the function of preprocessing an Excel file. First, it converts the addresses into lowercase letters to remove duplicates. Then, the rows with missing values are dropped; the duplicates are removed. The addresses that do not begin with ‘0x’ are removed as they do not represent a valid Ethereum address. The addresses are stored in a list.
    - Defines the function to process all files in the folder
    - Saves the list containing final addresses in the ‘ethereum_addresses.txt’ file

**Extract transactions for Ethereum addresses**
1.	Run the ‘Ethereum_transactions_extractor_json.py’ code to extract the transactions and save them to a text file. The ‘Ethereum_transactions_extractor_json.py’ code performs the following operations:
    - Reads the Ethereum addresses from the ‘ethereum_addresses.txt’ file
    - Extracts transactions for each address and saves the transactions to a CSV file.

**Convert JSON transaction data into text format**
1.	Run the ‘Ethereum_transactions_dataset.py’ code to extract the transactions and save them to a text file. The ‘Ethereum_transactions_dataset.py’ code performs the following operations:
    - Reads the Ethereum transactions data saved in the JSON format
    - Saves the transaction data in the text format

