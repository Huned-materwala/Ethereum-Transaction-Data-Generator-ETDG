import pandas as pd

# Load datasets
addresses_df = pd.read_csv('ETFD_nodal_features_per_address.txt', delimiter='\t')
transactions_df = pd.read_csv('feature_extraction_dataset.txt', delimiter="\t")

# Dictionary to map addresses to all features in addresses_df
address_to_features = addresses_df.set_index('address').to_dict(orient='index')

# Function to fetch all features based on address
def get_all_features(address):
    return address_to_features.get(address, None)

# Apply the function to 'from' column in transactions_df
transactions_df['all_features'] = transactions_df['from'].apply(get_all_features)

# Explode the 'all_features' column to create individual feature columns
transactions_df = pd.concat([transactions_df.drop(['all_features'], axis=1), transactions_df['all_features'].apply(pd.Series)], axis=1)

# Display or use transactions_df with added feature columns
print(transactions_df.head())
print(len(transactions_df))
print(len(transactions_df))

# Optionally, save the updated transactions_df to a new file
transactions_df.to_csv('ETFD_nodal_features.txt', sep="\t", index=False)
