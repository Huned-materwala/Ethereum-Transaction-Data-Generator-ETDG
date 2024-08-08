# Temporal and nodal features extraction

This step involves the execution of the following stages:
1. Generate a dataset for feature extraction
2. Extract temporal features
3. Extract nodal features per address
4. Extract nodal features
5. Generate ETFD dataset with extracted temporal and nodal features

---

**Generate a dataset for feature extraction**
1.	Run the ‘Feature_extraction_dataset.py’ code to generate a dataset for an efficient feature extraction. The ‘Feature_extraction_dataset.py’ code performs the following operations:
    - Reads the ‘ETFD_data_raw.txt’ file from the ‘Step 4_Raw dataset (Metadata)’ folder
    - Extracts the features required for temporal and nodal features extraction for each transaction. In particular, it extracts the following features: timestamp, from, to, value, and class labels.
    - Saves the resulting dataset with extracted features as ‘feature_extraction_dataset.txt’

**Extract temporal features**
1.	Run the ‘Temporal_features_extractor.py’ code to extract temporal features for the ETFD dataset. The ‘Temporal_features_extractor.py’ code performs the following operations:
    - Reads the ‘feature_extraction_dataset.txt’ file
    - For each transaction, it extracts the temporal features based on timestamp
    - Saves the dataset temporal features as ‘ETFD_temporal_features.txt’ file

**Extract nodal features per address**
1.	Run the ‘nodal_features_extractor.py’ code to extract nodal features per address for the ETFD dataset. The ‘nodal_features_extractor.py’ code performs the following operations:
    - Reads the ‘feature_extraction_dataset.txt’ file
    - For each transaction, it extracts the nodal features for the ‘from’ address
    - Saves the dataset with nodal features per address as ‘ETFD_nodal_features_per_address.txt’ file

**Extract nodal features**
1.	Run the ‘nodal_features_mapping.py’ code to map the nodal features per address with the transaction data. The ‘nodal_features_mapping.py’ code performs the following operations:
    - Reads the ‘feature_extraction_dataset.txt’ and the ‘ETFD_nodal_features_per_address.txt’ files
    - For each address in the ‘ETFD_nodal_features_per_address.txt’ file, it finds the corresponding transaction in ‘feature_extraction_dataset.txt’ file such that the ‘from’ address in the latter file is the same as the address from the former file
    - Appends the nodal features to the transaction data for that address
    - Saves the transaction data with nodal features as ‘ETFD_nodal_features’ file

**Generate ETFD dataset with extracted temporal and nodal features**
1.	Run the ETFD_extracted_features.py’ code to generate ETFD dataset with extracted temporal and nodal features. The ETFD_extracted_features.py’ code performs the following operations:
    - Reads the ‘ETFD_data_raw.txt’ file from the ‘Step4_Raw dataset (Metadata)’ folder. In addition, it reads the ‘ETFD_temporal_features.txt’ and ‘ETFD_nodal_features.txt’ files
    - For each transaction data, it combines the original features, temporal features, and nodal features
    - Saves the final ETFD dataset with extracted features as ‘ETFD_extracted_features.txt’ file

**NOTE: The files (that are over 100MB) related to this step can be downloaded from the following link: https://drive.google.com/drive/folders/16dImzEAupYAmsu2IN2pExQ5fbEaHN4XM?usp=drive_link**
