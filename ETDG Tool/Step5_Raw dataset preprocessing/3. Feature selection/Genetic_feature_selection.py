import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import os

# Load the dataset (assuming this part remains unchanged)
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file = os.path.join(dir, '2. Data balancing', 'ETFD_balanced.txt')

data = pd.read_csv(file, sep="\t", low_memory=False)
data['value'] = pd.to_numeric(data['value'], errors='coerce')

# Replace values in 'Fraud' column where 'No fraud' with 0 and Frauds with 1
data['Fraud'] = data['Fraud'].apply(lambda x: 0 if x == 'No Fraud' else 1)

# Define independent (X) features and dependent (y) variable
X = data.drop('Fraud', axis=1)
#X = x.apply(lambda x: (x - x.min()) / (x.max() - x.min()))  # normalize
y = data['Fraud']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Genetic Algorithm parameters
population_size = 10
num_generations = 100

# Initialize the population
def initialize_population(size, num_features):
    return np.random.randint(2, size=(size, num_features))

# Fitness function
def custom_genetic_fitness(solution, X_train_selected, X_test_selected, y_train, y_test):
    selected_features = [i for i in range(len(solution)) if solution[i] == 1]
    if len(selected_features) == 0:
        return 0
    
    # Train a classifier (example: Decision Tree)
    classifier = KNeighborsClassifier()
    classifier.fit(X_train_selected[:, selected_features], y_train)
    
    # Predict on the test set
    y_pred = classifier.predict(X_test_selected[:, selected_features])
    
    # Calculate confusion matrix to get FP and FN
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    
    # Calculate Precision and Recall
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # Calculate fitness
    fitness = 1/(fp * (1 - precision)**2 + fn * (1 - recall) + 1)
    
    return fitness, selected_features

# Main Genetic Algorithm loop
def genetic_algorithm(crossover_prob, mutation_prob):
    num_features = X_train.shape[1]
    population = initialize_population(population_size, num_features)
    best_solution = None
    best_fitness = 0
    best_selected_features = []
    fitness_history = []
    
    for generation in range(num_generations):
        fitness_scores = [custom_genetic_fitness(solution, X_train.values, X_test.values, y_train.values, y_test.values) for solution in population]
        fitness_scores, selected_features_list = zip(*fitness_scores)
        fitness_history.append(max(fitness_scores))
        
        # Keeping the best solutions from parents and offspring
        combined_population = population.copy()
        offspring_population = []
        
        while len(offspring_population) < population_size:
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)
            if random.random() < crossover_prob:
                child1, child2 = crossover(parent1, parent2)
                offspring_population.append(mutate(child1, mutation_prob))
                offspring_population.append(mutate(child2, mutation_prob))
        
        combined_population = np.vstack((combined_population, offspring_population))
        combined_fitness_scores = [custom_genetic_fitness(solution, X_train.values, X_test.values, y_train.values, y_test.values) for solution in combined_population]
        combined_fitness_scores, combined_selected_features_list = zip(*combined_fitness_scores)
        
        sorted_indices = np.argsort(combined_fitness_scores)[::-1]
        population = combined_population[sorted_indices[:population_size]]
        
        # Updating the best solution
        current_best_fitness = combined_fitness_scores[sorted_indices[0]]
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_solution = combined_population[sorted_indices[0]]
            best_selected_features = combined_selected_features_list[sorted_indices[0]]
        
        print(f"Generation {generation+1}: Best Fitness = {best_fitness}")
    
    return best_solution, best_fitness, best_selected_features, fitness_history

# Helper functions
def roulette_wheel_selection(population, fitness_scores):
    max_val = sum(fitness_scores)
    pick = random.uniform(0, max_val)
    current = 0
    for i, fitness_score in enumerate(fitness_scores):
        current += fitness_score
        if current > pick:
            return population[i]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2

def mutate(solution, mutation_prob):
    for i in range(len(solution)):
        if random.random() < mutation_prob:
            solution[i] = 1 - solution[i]
    return solution

# Test different combinations of crossover and mutation probabilities
crossover_probs = [0.8]
mutation_probs = [0.03]

results = []

# Run genetic algorithm for each combination
for crossover_prob in crossover_probs:
    for mutation_prob in mutation_probs:
        result = genetic_algorithm(crossover_prob, mutation_prob)
        results.append(result)

# Save fitness history for each combination to CSV files
for i, (crossover_prob, mutation_prob) in enumerate([(crossover_prob, mutation_prob) for crossover_prob in crossover_probs for mutation_prob in mutation_probs]):
    _, _, _, fitness_history = results[i]
    df_fitness = pd.DataFrame({'Generation': range(1, num_generations + 1), 'Fitness': fitness_history})
    filename = f'fitness_history_crossover_{crossover_prob}_mutation_{mutation_prob}.csv'
    df_fitness.to_csv(filename, index=False)

# Determine the best combination based on highest fitness and quickest convergence
best_fitness = -float('inf')
best_combination_index = None

for i, (crossover_prob, mutation_prob) in enumerate([(crossover_prob, mutation_prob) for crossover_prob in crossover_probs for mutation_prob in mutation_probs]):
    _, fitness, selected_features, _ = results[i]
    
    # Check if this combination has higher fitness or quicker convergence
    if fitness > best_fitness or (fitness == best_fitness and len(_) < len(results[best_combination_index][3])):
        best_fitness = fitness
        best_combination_index = i

# Retrieve best combination and its selected features
best_combination = (crossover_probs[best_combination_index // len(mutation_probs)], mutation_probs[best_combination_index % len(mutation_probs)])
_, _, best_selected_features, _ = results[best_combination_index]

print("Best Combination:")
print(f"Crossover Probability: {best_combination[0]}")
print(f"Mutation Probability: {best_combination[1]}")
print(f"Best Fitness: {best_fitness}")
print(f"Selected Features: {best_selected_features}")

with open('best_genetic_algorithm_results.txt', 'w') as file:
    file.write("Best Combination:\n")
    file.write(f"Crossover Probability: {best_combination[0]}\n")
    file.write(f"Mutation Probability: {best_combination[1]}\n")
    file.write(f"Best Fitness: {best_fitness}\n")
    file.write(f"Selected Features: {best_selected_features}\n")

print("Best combination, fitness, and features saved to best_genetic_algorithm_results.txt")

# Plot fitness over generations for the best combination
best_result = results[best_combination_index]

plt.figure(figsize=(10, 6))
plt.plot(range(1, num_generations + 1), best_result[3], marker='o', linestyle='-', color='b', label='Best Fitness')
plt.title('Fitness over Generations')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('fitness_best_plot.png')
plt.show()