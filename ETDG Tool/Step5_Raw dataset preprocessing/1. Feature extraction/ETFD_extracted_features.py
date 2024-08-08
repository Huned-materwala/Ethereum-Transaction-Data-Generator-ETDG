import pandas as pd
import os

# Read the dataset files
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
raw_data_file = os.path.join(dir, 'Step4_Raw dataset (Metadata)', 'ETFD_data_raw.txt')
raw_data = pd.read_csv(raw_data_file, sep=",", low_memory=False)
temporal_data = pd.read_csv("ETFD_temporal_features.txt", sep="\t", low_memory=False)
nodal_data = pd.read_csv("ETFD_nodal_features.txt", sep="\t", low_memory=False)

print(raw_data.columns)
print(temporal_data.columns)
print(nodal_data.columns)

# Selecting specific features from each dataframe
raw_data_selected = raw_data[['blockNumber', 'nonce','transactionIndex','value', 'gas',
                              'gasPrice', 'cumulativeGasUsed','gasUsed', 'confirmations', 'Fraud']]
temporal_data_selected = temporal_data[['Year', 'Month', 'Day', 'Hour', 'Minute']]
nodal_data_selected = nodal_data[['mean_value_sent', 'mean_value_received',
                                  'variance_value_sent', 'variance_value_received',
                                  'total_sent', 'total_received', 'time_diff_first_last_sent',
                                  'mean_time_between_sent', 'variance_time_between_sent', 'time_diff_first_last_received',
                                  'mean_time_between_received', 'variance_time_between_received',
                                  'total_tx_sent', 'total_tx_received', 'total_tx_sent_malicious', 'total_tx_received_malicious',
                                  'total_tx_sent_unique', 'total_tx_received_unique', 'total_tx_sent_malicious_unique',
                                  'total_tx_received_malicious_unique']]

# Concatenate dataframes horizontally
merged_df = pd.concat([raw_data_selected, temporal_data_selected, nodal_data_selected], axis=1)
merged_df.fillna(0, inplace=True)
# Display the merged dataframe
print(merged_df.head())

# Display the merged dataframe
print(merged_df.columns)
print(merged_df.dtypes)
print(merged_df.shape)
print(merged_df['Fraud'].value_counts())
print(merged_df.isnull().sum())

# Save the merged dataframe to a text file
merged_df.to_csv('ETFD_extracted_features.txt', sep='\t', index=False)
