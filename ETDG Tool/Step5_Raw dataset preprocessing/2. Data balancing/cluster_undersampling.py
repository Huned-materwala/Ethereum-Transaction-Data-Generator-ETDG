import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_classification
from sklearn.metrics import silhouette_score
from collections import Counter
import os

# Read the dataset file
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file = os.path.join(dir, '1. Feature extraction', 'ETFD_extracted_features.txt')

imbalanced_data = pd.read_csv(file, sep="\t", low_memory=False)

# Separate majority and minority classes
df_majority = imbalanced_data[imbalanced_data.Fraud == 'No Fraud']
df_minority = imbalanced_data[imbalanced_data.Fraud != 'No Fraud']

print(df_majority.shape)
print(df_minority.shape)

# Function to perform cluster-based undersampling
def cluster_based_undersampling(df_majority, df_minority, max_clusters=10):
    n_minority = len(df_minority)
    best_n_clusters = None
    best_inertia = np.inf
    best_clusters = None

    for n_clusters in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=1)
        cluster_labels = kmeans.fit_predict(df_majority.drop(columns='Fraud'))
        inertia = kmeans.inertia_

        if inertia < best_inertia:
            best_inertia = inertia
            best_n_clusters = n_clusters
            best_clusters = cluster_labels
    
    print(f'Optimal number of clusters: {best_n_clusters}')

    # Proportional sampling from clusters
    df_majority['cluster'] = best_clusters
    sampled_majority = pd.DataFrame()

    for cluster in range(best_n_clusters):
        cluster_samples = df_majority[df_majority.cluster == cluster]
        n_samples = int((len(cluster_samples) / len(df_majority)) * n_minority)
        sampled_cluster = cluster_samples.sample(n=n_samples, random_state=1)
        sampled_majority = pd.concat([sampled_majority, sampled_cluster], axis=0)
    
    # Combine undersampled majority class with minority class
    undersampled_df = pd.concat([sampled_majority.drop(columns='cluster'), df_minority], axis=0)
    return undersampled_df

# Apply the function
balanced_df = cluster_based_undersampling(df_majority, df_minority)

# Verify the class distribution
print("Class distribution after undersampling:")
print(Counter(balanced_df['Fraud']))

# Save the merged dataframe to a text file
balanced_df.to_csv('ETFD_balanced.txt', sep='\t', index=False)