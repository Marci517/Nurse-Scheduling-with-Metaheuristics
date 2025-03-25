# Documentation: Nurse Scheduling Problem

## Problem Description

The goal of the nurse scheduling problem is to create an optimal work schedule for nurses in a hospital. The schedule must satisfy the following constraints:

### Hard Constraints:
- A nurse can only work one shift per day (morning, afternoon, night).
- A nurse cannot work a night shift followed by a morning shift.

### Soft Constraints:
- A nurse cannot work more than 7 consecutive days.

---

## Algorithm Descriptions

### 1. Simulated Annealing (SA)
This is a metaheuristic search algorithm aimed at finding the global optimum. The algorithm starts by making large changes to the solutions and gradually makes smaller modifications as the temperature decreases. SA allows accepting worse solutions at the beginning, helping avoid local optima traps.

#### Steps:
1. Generate an initial solution.
2. Generate new solutions in each iteration.
3. Decide whether to accept the solution based on the acceptance criterion.
4. Decrease the temperature over time.

### 2. Ant Colony Optimization (ACO)
This algorithm is based on the behavior of ants in nature. Ants leave pheromones behind, which influence the path other ants choose to follow.

#### Steps:
1. Initialize pheromone values.
2. Multiple ants attempt to build a solution in each iteration.
3. Update pheromone levels based on the best solutions.
4. Evaluate the best solution at the end of the iterations.

### 3. Ant Colony Optimization Min-Max Version (ACO Min-Max)
This is an enhanced version of the standard ACO algorithm where pheromone values are kept within a minimum and maximum boundary. This helps maintain more balanced pheromone distribution.

#### Steps:
1. Set initial pheromone values to the maximum.
2. Multiple ants attempt to build a solution in each iteration.
3. Update pheromones based on the best solution.
4. Evaluate the best solution at the end of the iterations.

### 4. Grey Wolf Optimization (GWO)
This algorithm is based on the hunting strategy of grey wolves. Wolves work in a hierarchical structure to cooperatively search for the best solution.

#### Steps:
1. Generate an initial population.
2. The population moves toward the best solution under the guidance of alpha, beta, and delta wolves.
3. Update positions relative to the leading wolves.
4. Improve the solution over iterations.

### 5. Combined Simulated Annealing and Genetic Algorithm (SA+GA)
This hybrid algorithm combines Simulated Annealing and Genetic Algorithm, taking advantage of both techniques. SA performs local search, while GA maintains population diversity.

#### Steps:
1. Generate an initial population.
2. Apply genetic operators (crossover and mutation).
3. Refine the GA-generated solutions using Simulated Annealing.
4. Select the best solution over generations.

---

## Parameters and Test Cases

### Parameters

#### Simulated Annealing:
- Initial temperature: 1,000,000
- Cooling schedule: linear, alpha = 1
- Number of iterations: 200,000

#### Ant Colony Optimization:
- Number of ants: 40
- Pheromone evaporation rate: 0.9
- alpha = 1 (pheromone influence)
- beta = 2 (heuristic influence)
- Number of iterations: 500

#### Ant Colony Optimization Min-Max:
- Number of ants: 40
- Pheromone evaporation rate: 0.9
- Pheromone limits: [0.1, 5.0]
- alpha = 1
- beta = 2
- Number of iterations: 500

#### Grey Wolf Optimization:
- Population size: 20
- Number of iterations: 200
- Attraction parameter (a): 2

#### SA+GA:
- Population size: 20
- Generation size: 20
- Mutation rate: 0.1
- SA initial temperature: 1,000,000
- Number of iterations: 200,000
- Cooling schedule: exponential, alpha = 0.85

### Test Cases
- **Small size:** 5 nurses, 7 days
- **Medium size:** 50 nurses, 30 days
- **Large size:** 200 nurses, 300 days

---

## Results

The penalty is calculated using the quality function:


The penalty is calculated using the quality function:

| Test Case        | Algorithm            | Execution Time (s) | Penalty Points |
|------------------|----------------------|--------------------|----------------|
| Small            | Simulated Annealing  | 2.8                | 0              |
| Small            | ACO                  | 0.84               | 0              |
| Small            | ACO Min-Max          | 0.85               | 0              |
| Small            | GWO                  | 0.13               | 0              |
| Small            | SA+GA                | 0.01               | 0              |
| Medium           | Simulated Annealing  | 109.3              | 11,500         |
| Medium           | ACO                  | 51.9               | 22,900         |
| Medium           | ACO Min-Max          | 52.2               | 23,400         |
| Medium           | GWO                  | 3.4                | 11,500         |
| Medium           | SA+GA                | 0.44               | 23,300         |
| Large            | Simulated Annealing  | 4822.6             | 612,300        |
| Large            | ACO                  | 2325.8             | 1,222,800      |
| Large            | ACO Min-Max          | 2362.1             | 1,222,000      |
| Large            | GWO                  | 137.7              | 590,600        |
| Large            | SA+GA                | 16.4               | 1,216,900      |

---

## Conclusions and Future Goals

### Conclusions
- Simulated Annealing is much slower than the other algorithms due to the linear cooling schedule but produces one of the most optimal results.
- ACO provides stable results thanks to its pheromone update mechanism. It's relatively fast for small/medium inputs, but it slows down significantly for large inputs.
- ACO Min-Max does not show significant improvement over basic ACO and is slightly slower.
- GWO effectively converges to the best solution. It is the winner in this "competition."
- The SA+GA hybrid generates results close to ACO but is much faster due to the exponential cooling in SA.

### Future Goals
- Fine-tuning the algorithms by optimizing parameter settings.
- Adding more constraints to simulate real-world hospital scenarios.
- Parallelizing algorithms to reduce runtime.
- Optimizing or replacing the cooling function used in the SA part of hybrid algorithms.
