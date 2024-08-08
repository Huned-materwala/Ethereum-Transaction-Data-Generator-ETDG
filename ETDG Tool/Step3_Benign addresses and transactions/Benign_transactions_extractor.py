import os
import pandas as pd
import concurrent.futures
from tqdm import tqdm


# Read all text files from a directory and combine them into a DataFrame

# Get the current directory of the script (main_script.py)
current_dir = os.path.dirname(os.path.realpath(__file__))
# Navigate to the parent directory
parent_dir = os.path.dirname(current_dir)
# Construct the path to dataset_folder
dataset_folder_path = os.path.join(parent_dir, 'Step2_Ethereum addresses and transactions', 'Ethereum transactions_dataset')
files_directory = dataset_folder_path

dataframes = []
# Loop through all files in the directory
for filename in os.listdir(files_directory):
    if filename.endswith(".txt"):  # Check if the file is a text file
        file_path = os.path.join(files_directory, filename)
        # Read the text file into a dataframe with specified dtypes
        df = pd.read_csv(file_path, sep='\t', low_memory=False)  # Modify the separator based on your file's structure
        dataframes.append(df)

# Concatenate all dataframes into one
combined_df = pd.concat(dataframes, ignore_index=True)
print(combined_df.dtypes)

# Function to process the dataset
def process_dataset(df, malicious_addresses_file):
    # Lowercase 'from' and 'to' columns with progress bar
    tqdm.pandas(desc="Lowercasing addresses")
    df['from'] = df['from'].progress_apply(lambda x: x.lower() if isinstance(x, str) else x)
    df['to'] = df['to'].progress_apply(lambda x: x.lower() if isinstance(x, str) else x)
    
    # Load malicious addresses from file
    with open(malicious_addresses_file, 'r') as f:
        malicious_addresses = set(f.read().strip().split('\n'))
    
    # Count rows and features before processing
    rows_before = len(df)
    features_before = len(df.columns)
    
    # Progress bar for row filtering
    tqdm.pandas(desc="Filtering rows")
    df = df[~df.progress_apply(lambda row: row['from'] in malicious_addresses or row['to'] in malicious_addresses, axis=1)]
    
    # Count rows and features after processing
    rows_after = len(df)
    features_after = len(df.columns)
    
    return df, rows_before, features_before, rows_after, features_after

# Function to coordinate parallel processing
def parallel_process(combined_df, malicious_addresses_file):
    # Step: Process the combined dataset
    df_processed, rows_before, features_before, rows_after, features_after = process_dataset(combined_df, malicious_addresses_file)
    return df_processed, rows_before, features_before, rows_after, features_after

if __name__ == '__main__':
    malicious_addresses_file = 'malicious_addresses.txt'
    
    # Use ThreadPoolExecutor for concurrent processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(parallel_process, combined_df, malicious_addresses_file)
        df_processed, rows_before, features_before, rows_after, features_after = future.result()
    
    # Print number of rows and features before and after processing
    print(f"Number of rows before processing: {rows_before}")
    print(f"Number of features before processing: {features_before}")
    print(f"Number of rows after processing: {rows_after}")
    print(f"Number of features after processing: {features_after}")
    
    # Save processed dataset to a new text file
    output_file = 'benign_transactions.txt'
    df_processed.to_csv(output_file, sep='\t', index=False)


'''
import os
import pandas as pd
import concurrent.futures
from tqdm import tqdm

# Function to read all text files from a directory and combine them into a DataFrame
def combine_text_files(directory):
    combined_data = []
    # List all text files
    file_list = [filename for filename in os.listdir(directory) if filename.endswith('.txt')]
    for filename in tqdm(file_list, desc="Combining files"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            # Assuming each file contains tab-separated data
            data = file.read().strip().split('\n')
            combined_data.extend(data)
    
    # Create a DataFrame from the combined data
    df = pd.DataFrame([entry.split('\t') for entry in combined_data])
    # Assuming the first row in each file is the header, set it as the column names
    df.columns = df.iloc[0]
    df = df[1:]  # Remove the duplicated header row
    
    return df

# Function to process the dataset
def process_dataset(df, malicious_addresses_file):
    # Lowercase 'from' and 'to' columns with progress bar
    tqdm.pandas(desc="Lowercasing addresses")
    df['from'] = df['from'].progress_apply(lambda x: x.lower())
    df['to'] = df['to'].progress_apply(lambda x: x.lower())
    
    # Load malicious addresses from file
    with open(malicious_addresses_file, 'r') as f:
        malicious_addresses = set(f.read().strip().split('\n'))
    
    # Count rows and features before processing
    rows_before = len(df)
    features_before = len(df.columns)
    
    # Progress bar for row filtering
    tqdm.pandas(desc="Filtering rows")
    df = df[~df.progress_apply(lambda row: row['from'] in malicious_addresses or row['to'] in malicious_addresses, axis=1)]
    
    # Count rows and features after processing
    rows_after = len(df)
    features_after = len(df.columns)
    
    return df, rows_before, features_before, rows_after, features_after

# Function to coordinate parallel processing
def parallel_process(files_directory, malicious_addresses_file):
    # Step 1: Combine text files into a DataFrame
    df = combine_text_files(files_directory)
    
    # Step 2: Process the combined dataset
    df_processed, rows_before, features_before, rows_after, features_after = process_dataset(df, malicious_addresses_file)
    
    return df_processed, rows_before, features_before, rows_after, features_after

# Function to coordinate parallel processing
def parallel_process(files_directory, malicious_addresses_file):
    # Step 1: Combine text files into a DataFrame
    df = combine_text_files(files_directory)
    
    # Step 2: Process the combined dataset
    df_processed, rows_before, features_before, rows_after, features_after = process_dataset(df, malicious_addresses_file)
    
    return df_processed, rows_before, features_before, rows_after, features_after

if __name__ == '__main__':
    # Get the current directory of the script (main_script.py)
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Navigate to the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Construct the path to dataset_folder
    dataset_folder_path = os.path.join(parent_dir, 'Step2_Ethereum addresses and transactions', 'Ethereum transactions_dataset_temp')
    
    files_directory = dataset_folder_path
    malicious_addresses_file = 'malicious_addresses.txt'
    
    
    # Use ThreadPoolExecutor for concurrent processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(parallel_process, files_directory, malicious_addresses_file)
        df_processed, rows_before, features_before, rows_after, features_after = future.result()
    
    # Print number of rows and features before and after processing
    print(f"Number of rows before processing: {rows_before}")
    print(f"Number of features before processing: {features_before}")
    print(f"Number of rows after processing: {rows_after}")
    print(f"Number of features after processing: {features_after}")
    
    # Save processed dataset to a new text file
    output_file = 'benign_transactions.txt'
    df_processed.to_csv(output_file, sep='\t', index=False)
'''