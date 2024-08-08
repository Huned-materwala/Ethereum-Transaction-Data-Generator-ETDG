# Feature selection

This step comprises of two stages:
1. Perform feature selection using Genetic Algorithm
2. Generate ETFD dataset with selected features

---

**Perform feature selection using Genetic Algorithm**
1.	Run the ‘Genetic_feature_selection.py’ code to perform feature selection using genetic algorithm. The ‘Genetic_feature_selection.py’ code performs the following operations:
    - Reads the ‘ETFD_balanced.txt’ file from ‘2. Data balancing’ folder
    - Performs genetic algorithm with the proposed novel fitness function on the balanced dataset
    - Saves the optimal crossover rate, mutation rate, fitness value, and selected features in a csv file

**Generate ETFD dataset with selected features**
1.	Run the ‘ETFD_Dataset.py’ code to generate the final dataset with selected features. The ‘ETFD_Dataset.py’ code performs the following operations:
    - Reads the ‘ETFD_balanced.txt’ file from ‘2. Data balancing’ folder
    - Selects the features selected by the genetic algorithm
    - Saves the final dataset as ‘ETFD_Dataset.txt’ file
