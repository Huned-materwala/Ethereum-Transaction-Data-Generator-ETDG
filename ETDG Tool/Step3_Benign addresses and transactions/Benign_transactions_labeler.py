import pandas as pd

# Load the dataset
input_file_path = 'benign_transactions.txt'
df = pd.read_csv(input_file_path, delimiter='\t', low_memory=False)

# Add the 'Fraud' column with 'No Fraud' as the default value for all rows
df['Fraud'] = 'No Fraud'

# Save the updated dataframe to a new text file
output_file_path = 'benign_transactions_preprocessed_labeled.txt'
df.to_csv(output_file_path, index=False, sep='\t')
print("Dataset has been updated and saved to", output_file_path)

# Print the total number of rows in the combined dataset
total_rows = len(df)
print(f"Total number of rows in the combined dataset: {total_rows}")
print(df.dtypes)