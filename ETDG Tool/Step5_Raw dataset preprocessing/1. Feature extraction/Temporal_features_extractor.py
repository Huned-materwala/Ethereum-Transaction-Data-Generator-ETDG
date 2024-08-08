import pandas as pd

# Read the text file
df = pd.read_csv("feature_extraction_dataset.txt", delimiter="\t")

# Keep only the timestamp column
timestamps = df["timeStamp"]

# Convert timestamps to datetime format
timestamps = pd.to_datetime(timestamps, unit='s', errors='coerce')  # Assuming timestamps are in seconds

# Create a new DataFrame with decomposed features
new_df = pd.DataFrame({
    "Year": timestamps.dt.year,
    "Month": timestamps.dt.month,
    "Day": timestamps.dt.day,
    "Hour": timestamps.dt.hour,
    "Minute": timestamps.dt.minute
})

# Store the new dataset in a text file
new_df.to_csv("ETFD_temporal_features.txt", sep="\t", index=False)

# Print the shape of the new dataset
print("Shape of the new dataset:", new_df.shape)