# Malicious addresses and transactions extraction

This step involves the execution of the following stages:
1. Collect the list of malicious addresses and corresponding fraud categories
2. Extract transactions for malicious addresses
3. Label malicious transactions based on the fraud description
4. Preprocess labeled malicious

---

**Collect the list of malicious addresses and the corresponding fraud categories**
1.	Go to the EtherScamDB GitHub repository (https://github.com/MrLuit/EtherScamDB)
2.	Navigate to the ‘_data’ folder and download the ‘scams.yaml’ file
3.	Run the ‘Malicious_addresses_category_extractor.py’ code to generate a list of malicious addresses and the corresponding fraud category. The ‘Malicious_addresses_category_extractor.py’ code performs the following operations:
    - Opens the YAML file and loads the data
    - Extracts the addresses and corresponding fraud categories
    - Replaces the ‘Scam’ category with ‘Scamming’ (This is because there exists ‘Scam’ and ‘Scamming’ categories in the ‘scams.yaml’ file. However, both of them represent the same fraud category. Consequently, ‘Scamming’ is used to represent both categories.)
    - Removes the addresses that do not begin with ‘0x’ as they do not represent a valid Ethereum address
    - Converts the addresses to lowercase to identify duplicates
    - Removes duplicate addresses
    - Saves the list of unique malicious addresses and the corresponding categories to ‘malicious_addresses_and_categories.csv’ file

**Extract transactions for malicious addresses**
1.	Run the ‘Malicious_transactions_extractor.py’ code to extract the transactions for malicious addresses and save them in a CSV file. The ‘Malicious_transactions_extractor.py’ code performs the following operations:
    - Defines the function to extract transactions for an address using Etherscan API
    - Reads the malicious addresses from the ‘malicious_addresses_and_categories.csv’ file
    - Extracts transactions for each address and appends them to a list
    - Saves the list to a ‘malicious_transactions.csv’ file

**Label malicious transactions based on the fraud description**
1.	Run the ‘Malicious_transactions_labeler.py’ code to label the malicious transactions based on the fraud categories. The ‘Malicious_transactions_labeler.py’ code performs the following operations:
    - Loads addresses and corresponding fraud categories from 'malicious_addresses_and_categories.csv' file
    - Makes a copy of the 'malicious_transactions.csv' file to store the labeled dataset. The copied file is named ‘malicious_transactions_labeled.csv’
    - Updates 'malicious_transactions_labeled.csv' with the 'Fraud' column to store the fraud category labels
    - For each transaction, the code checks the sender and receiver addresses. If one of the sender or receiver addresses is present in the 'malicious_addresses_and_categories.csv' file, the fraud category for that address is assigned in the ‘Fraud’ column. If both the addresses are present in the 'malicious_addresses_and_categories.csv' file, then ‘multi-category’ is assigned to the ‘Fraud’ column if the category for both addresses is different; otherwise, the category is assigned. If none of the addresses are present, then ‘Null’ is assigned.

**Preprocess labeled malicious**
1.	Run the ‘Malicious_transactions_preprocessor.py’ code to preprocess labeled malicious transactions. The ‘Malicious_transactions_preprocessor.py’ code performs the following operations:
    - Loads labeled malicious transactions from ‘malicious_transactions_labeled.csv’ file
    - Removes the transactions where iserror = 1 or value = 0
    - Saves the preprocessed malicious transactions in ‘malicious_transactions_preprocessed_labeled.csv’ file
