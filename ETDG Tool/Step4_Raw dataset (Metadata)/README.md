# Ethereum transaction raw dataset (without feature extraction, data balancing, and feature selection)

This step involves the execution of the following stage:
1. Generate raw ETFD dataset

---

**Generate raw ETFD dataset**
1.	Run the ‘ETFD_data_raw.py’ code to generate the raw ETFD dataset. The ‘ETFD_data_raw.py’ code performs the following operations:
    - Reads the ‘malicious_transactions_preprocessed_labeled.csv’ and ‘benign_transactions_preprocessed_labeled.txt’ files from ‘Step1_Malicious addresses and transactions’ and ‘Step3_Benign addresses and transactions’ folders, respectively
    - Combines both files and saves it as ‘ETFD_data_raw.txt’ file
