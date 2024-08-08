import pandas as pd
import os

# Get the dataset path
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(dir)
file_name = 'ETFD_data_raw.txt'
data = os.path.join(dir, 'Step4_Raw dataset (Metadata)', file_name)


# Read the text file
df = pd.read_csv(data, sep=",", low_memory=False)

# Select only the required columns
selected_df = df[["timeStamp", "from", "to", "value", "Fraud"]]

# Save the selected dataframe to a new text file
selected_df.to_csv("feature_extraction_dataset.txt", sep="\t", index=False)

# Print the shape of the selected dataframe
print("Shape of selected dataframe:", selected_df.shape)