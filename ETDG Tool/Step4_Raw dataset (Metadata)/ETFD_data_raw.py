import pandas as pd
import os

# Define file paths

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(dir)


csv_file_path = os.path.join(dir, 'Step1_Malicious addresses and transactions', 'malicious_transactions_preprocessed_labeled.csv')
text_file_path = os.path.join(dir, 'Step3_Benign addresses and transactions', 'benign_transactions_preprocessed_labeled.txt')

# Function to read large files
def read_large_file(file_path, delimiter=','):
    try:
        return pd.read_csv(file_path, delimiter=delimiter, low_memory=False)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

# Load the datasets
csv_df = read_large_file(csv_file_path)  # CSV is comma-separated
text_df = read_large_file(text_file_path, delimiter='\t')  # Text file is tab-separated

# Check if dataframes are loaded properly
if csv_df.empty:
    print("CSV file couldn't be read.")
if text_df.empty:
    print("Text file couldn't be read.")

# Combine the datasets if both are loaded properly
if not csv_df.empty and not text_df.empty:
    # Ensure combined DataFrame columns match CSV file's data types
    text_df = text_df[csv_df.columns]  # Align columns to match CSV file
    
    # Concatenate CSV and aligned text DataFrames
    combined_df = pd.concat([csv_df, text_df], ignore_index=True)
    
    # Save the combined dataframe to a new text file
    output_file_path = 'ETFD_data_raw.txt'
    combined_df.to_csv(output_file_path, index=False, sep=',')
    
    # Print the shape of the datasets
    print("Shape of CSV file:", csv_df.shape)
    print("Shape of text file:", text_df.shape)
    print(combined_df.dtypes)
    print("Shape of combined file:", combined_df.shape)
else:
    print("Combination skipped due to read errors.")
