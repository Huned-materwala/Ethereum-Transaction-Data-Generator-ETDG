import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('feature_extraction_dataset.txt', delimiter="\t")

# Function to clean and convert values to numeric
def clean_and_convert(value):
    try:
        # Multiply by 1e-18 and then convert to float
        cleaned_value = float(value) * 1e-18
        return cleaned_value
    except Exception as e:
        print(f"Could not convert value '{value}' to numeric: {e}")
        return np.nan  # Return NaN for values that cannot be converted

# Clean and convert 'value' column
df['value'] = df['value'].apply(clean_and_convert)

# Drop rows with NaN values in 'value' column
df.dropna(subset=['value'], inplace=True)

# Read malicious addresses from a text file
with open('malicious_addresses.txt', 'r') as file:
    malicious_addresses = file.read().splitlines()


addresses = pd.concat([df['from'], df['to']]).unique()

# Define features and initialize a list to store dictionaries of each address
features = ['address', 'mean_value_sent', 'mean_value_received', 'variance_value_sent',
            'variance_value_received', 'total_sent', 'total_received', 'time_diff_first_last_sent',
            'mean_time_between_sent', 'variance_time_between_sent', 'time_diff_first_last_received',
            'mean_time_between_received', 'variance_time_between_received',
            'total_tx_sent', 'total_tx_received', 'total_tx_sent_malicious', 'total_tx_received_malicious',
            'total_tx_sent_unique', 'total_tx_received_unique', 'total_tx_sent_malicious_unique',
            'total_tx_received_malicious_unique']

data_list = []

i = 1
total_addresses = len(addresses)
for address in addresses:
    sent_transactions = df[df['from'] == address]
    received_transactions = df[df['to'] == address]
    
    sent_values = sent_transactions['value']
    received_values = received_transactions['value']
    sent_timestamps = sent_transactions['timeStamp']
    received_timestamps = received_transactions['timeStamp']

    if not sent_timestamps.empty:
        sent_time_diffs = np.diff(np.sort(sent_timestamps)) / 86400  # Convert to days
    else:
        sent_time_diffs = np.array([])  # Empty array if no sent timestamps
    
    if not received_timestamps.empty:
        received_time_diffs = np.diff(np.sort(received_timestamps)) / 86400  # Convert to days
    else:
        received_time_diffs = np.array([])  # Empty array if no received timestamps

     # Count total sent transactions and total received transactions
    total_transactions_sent = len(sent_transactions)
    total_transactions_received = len(received_transactions)
    
    # Count total transactions sent to unique addresses and received from unique addresses
    total_transactions_sent_to_unique_address = sent_transactions['to'].nunique()
    total_transactions_received_from_unique_address = received_transactions['from'].nunique()
    
    # Count total sent transactions to and total received transactions from malicious addresses
    total_transactions_sent_to_malicious_address = len(sent_transactions[sent_transactions['to'].isin(malicious_addresses)])
    total_transactions_received_from_malicious_address = len(received_transactions[received_transactions['from'].isin(malicious_addresses)])

    # Count total sent transactions to and total received transactions from unique malicious addresses
    total_transactions_sent_to_unique_malicious = len(sent_transactions[sent_transactions['to'].isin(malicious_addresses)]['to'].unique())
    total_transactions_received_from_unique_malicious = len(received_transactions[received_transactions['from'].isin(malicious_addresses)]['from'].unique())

    # Define a mapping dictionary with values for each feature
    value_map = {
        'address': address,
        'total_sent': sent_values.sum(),
        'mean_value_sent': sent_values.mean(),
        'variance_value_sent': sent_values.var(),
        'total_received': received_values.sum(),
        'mean_value_received': received_values.mean(),
        'variance_value_received': received_values.var(),
        'time_diff_first_last_sent': (max(sent_timestamps) - min(sent_timestamps)) / 86400 if not sent_timestamps.empty else np.nan,
        'mean_time_between_sent': sent_time_diffs.mean() if len(sent_time_diffs) > 0 else np.nan,
        'variance_time_between_sent': sent_time_diffs.var() if len(sent_time_diffs) > 0 else np.nan,
        'time_diff_first_last_received': (max(received_timestamps) - min(received_timestamps)) / 86400 if not received_timestamps.empty else np.nan,
        'mean_time_between_received': received_time_diffs.mean() if len(received_time_diffs) > 0 else np.nan,
        'variance_time_between_received': received_time_diffs.var() if len(received_time_diffs) > 0 else np.nan,
        'total_tx_sent': total_transactions_sent,
        'total_tx_received': total_transactions_received,
        'total_tx_sent_malicious': total_transactions_sent_to_malicious_address,
        'total_tx_received_malicious': total_transactions_received_from_malicious_address,
        'total_tx_sent_unique': total_transactions_sent_to_unique_address,
        'total_tx_received_unique': total_transactions_received_from_unique_address,
        'total_tx_sent_malicious_unique': total_transactions_sent_to_unique_malicious,
        'total_tx_received_malicious_unique': total_transactions_received_from_unique_malicious,
    }


    # Append the mapping dictionary to the list
    data_list.append(value_map)

    # Calculate and print progress percentage
    progress = i / total_addresses * 100
    print(f"Progress: {progress:.2f}%")
    
    i += 1

# Convert the list of dictionaries to a DataFrame
df_features = pd.DataFrame(data_list, columns=features)

# Save the DataFrame to a text file
df_features.to_csv('ETFD_nodal_features_per_address.txt', sep='\t', index=False)