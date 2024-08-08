# Benign addresses and transactions extraction

This step involves the execution of the following stages:
1. Extract benign transactions
2. Label benign transactions

---

**Extract benign transactions**
1.	Run the ‘Benign_transactions_extractor.py’ code to extract and save the benign transactions in a text file. The ‘Benign_transactions_extractor.py’ code performs the following operations:
    - Reads the ‘Ethereum transactions_dataset.txt’ file from the ‘Step2_Ethereum addresses and transactions’ folder
    - Converts the ‘from’ and ‘to’ addresses to lowercase
    - Removes the transactions with ‘from’ or ‘to’ addresses in the ‘malicious_addresses.txt’ file.
    - Saves the resultant transaction data into ‘benign_transactions.txt’ file

**Label benign transactions**
1.	Run the ‘Benign_transactions_labeler.py’ code to label the benign transactions. The ‘Benign_transactions_labeler.py’ performs the following operations:
    - Reads the ‘benign_transactions.txt’ file
    - For each transaction, it adds a class label ‘No Fraud’
    - Saves the labeled dataset to ‘benign_transactions_preprocessed_labeled.txt’ file

**NOTE: The files (that are over 100MB) related to this step can be downloaded from the following link: https://drive.google.com/drive/folders/13QVj5LOAc8tx5ho_o4Z_2paEBNtqKUMk?usp=drive_link**
