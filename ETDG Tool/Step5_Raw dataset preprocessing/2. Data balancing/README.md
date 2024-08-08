# Data balancing

This step involves execution of the following stage:
1. Generate balanced ETFD dataset

---

**Generate balanced ETFD dataset**
1.	Run the ‘cluster_undersampling.py’ code to generate the balanced ETFD dataset. The ‘cluster_undersampling.py’ code performs the following operations:
    - Reads the ‘ETFD_extracted_feature.txt’ file from ‘1. Feature extraction’ folder
    - Performs clustered undersampling and saves the balanced dataset in the ‘ETFD_balanced.txt’ file
