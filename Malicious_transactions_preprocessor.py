import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'malicious_transactions_labeled.csv'
df = pd.read_csv(file_path)

# Print the number of transactions before filtering
print(f"Number of transactions before filtering: {len(df)}")

# Filter out rows where 'isError' is 1 or 'value' is 0
df_filtered = df[(df['isError'] != 1) & (df['value'] != '0')]

# Print the number of transactions after filtering
print(f"Number of transactions after filtering: {len(df_filtered)}")

# Save the filtered DataFrame back to a CSV file
output_file_path = 'malicious_transactions_preprocessed_labeled.csv'
df_filtered.to_csv(output_file_path, index=False)