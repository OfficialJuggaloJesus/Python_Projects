import numpy as np

# Define the objective function to optimize
def objective_function(x):
    return -x**2 + 10*x  # Example function: -x^2 + 10x

# Genetic algorithm parameters
population_size = 20
num_generations = 50
mutation_rate = 0.1
crossover_rate = 0.7

# Initialize population
def initialize_population(size):
    return np.random.uniform(0, 10, size=(size,))

# Evaluate fitness of the population
def evaluate_population(population):
    return np.array([objective_function(ind) for ind in population])

# Select parents for crossover
def select_parents(population, fitness):
    idx = np.argsort(fitness)[-2:]  # Select the best 2 individuals
    return population[idx]

# Perform crossover to produce offspring
def crossover(parent1, parent2):
    if np.random.rand() < crossover_rate:
        return (parent1 + parent2) / 2
    else:
        return parent1 if np.random.rand() < 0.5 else parent2

# Perform mutation
def mutate(individual):
    if np.random.rand() < mutation_rate:
        return individual + np.random.normal(0, 1)
    else:
        return individual

# Genetic Algorithm
def genetic_algorithm():
    population = initialize_population(population_size)
    for generation in range(num_generations):
        fitness = evaluate_population(population)
        best_individual = population[np.argmax(fitness)]
        print(f"Generation {generation}: Best fitness = {np.max(fitness)}, Best individual = {best_individual}")
        
        new_population = []
        for _ in range(population_size):
            parents = select_parents(population, fitness)
            offspring = crossover(parents[0], parents[1])
            offspring = mutate(offspring)
            new_population.append(offspring)
        
        population = np.array(new_population)
    
    return best_individual

# Run the genetic algorithm
best_solution = genetic_algorithm()
print(f"Best solution found: {best_solution}")
