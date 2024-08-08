# Import libraries
import pandas as pd
import numpy as np
import os

# Get the dataset path
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file = os.path.join(dir, '2. Data balancing', 'ETFD_balanced.txt')

# Import dataset
data = pd.read_csv(data, sep="\t", low_memory=False)
X = data.drop('Fraud', axis=1)
y = data['Fraud']

# List of column indices to keep
columns_to_keep = [0, 8, 10, 11, 12, 15, 17, 19, 23, 26, 28, 30, 32, 33]

# Select the columns using iloc
data_feature_selection = X.iloc[:, columns_to_keep]
print(data_feature_selection.columns)
data_feature_selection['Fraud'] = data['Fraud'] # add fraud label
print(data_feature_selection.shape)
print(data_feature_selection.columns)

# Binary classification dataset (values in 'Fraud' column where 'No fraud' with 0 and Frauds with 1)
data_binary = data_feature_selection.copy()
data_binary['Fraud'] = data_binary['Fraud'].apply(lambda x: 0 if x == 'No Fraud' else 1)
data_binary.to_csv('ETMFD_Dataset.txt', sep='\t', index=False)

'''
# Multi-class classification dataset (values in 'Fraud' column where 'No fraud' with 0 and Frauds with 1)
data_multiclass = data_feature_selection.copy()
data_multiclass.to_csv('ETMFD_multiclass_truncate.txt', sep='\t', index=False)
'''