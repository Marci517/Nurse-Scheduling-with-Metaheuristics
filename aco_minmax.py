import random
import time


def quality(hard_constraints, soft_constraints):
    return hard_constraints * 100 + soft_constraints * 10


def check_constraints(schedule):
    hard_constraints = 0
    soft_constraints = 0

    for nurse, shifts in schedule.items():
        for day_idx in range(len(shifts) - 1):
            if shifts[day_idx] == 'N' and shifts[day_idx + 1] == 'M':
                hard_constraints += 1
            if day_idx >= 7:
                days = shifts[day_idx - 7: day_idx + 1]
                if all(shift in ['M', 'A', 'N'] for shift in days):
                    soft_constraints += 1

    return hard_constraints, soft_constraints


def generate_solution(nurses, days, shifts, pheromones, alpha, beta):
    schedule = {nurse: [] for nurse in nurses}
    for day in range(days):
        for nurse in nurses:
            probabilities = []
            cumulative_probabilities = []

            for shift in shifts:
                pheromone_level = pheromones[(nurse, day, shift)] ** alpha
                heuristic = random.random() ** beta  # Simplified heuristic value
                probabilities.append((shift, pheromone_level * heuristic))

            total = sum(value for _, value in probabilities)

            normalized_probabilities = []
            for shift, value in probabilities:
                normalized_probabilities.append((shift, value / total))

            cumulative = 0
            for shift, value in normalized_probabilities:
                cumulative += value
                cumulative_probabilities.append((shift, cumulative))

            random_value = random.random()
            selected_shift = None
            for shift, value in cumulative_probabilities:
                if random_value < value:
                    selected_shift = shift
                    break

            schedule[nurse].append(selected_shift)

    return schedule


start = time.time()
nurses = ['N1', 'N2', 'N3', 'N4']
days = 10
shifts = ['M', 'A', 'N']  # Morning, Afternoon, Night
population_size = 20
alpha = 1
beta = 2
iterations = 500
min_pheromone = 0.1
max_pheromone = 5.0
pheromones = {}
for nurse in nurses:
    for day in range(days):
        for shift in shifts:
            pheromones[(nurse, day, shift)] = max_pheromone

best_schedule = None
best_quality = float('inf')

for iteration in range(iterations):
    population = []
    for pop_idx in range(population_size):
        schedule = generate_solution(nurses, days, shifts, pheromones, alpha, beta)
        hard, soft = check_constraints(schedule)
        current_quality = quality(hard, soft)

        if current_quality < best_quality:
            best_schedule = schedule
            best_quality = current_quality
        population.append((schedule, current_quality))

    # Evaporate pheromones
    for nurse in nurses:
        for day in range(days):
            for shift in shifts:
                pheromones[(nurse, day, shift)] *= 0.8
                if pheromones[(nurse, day, shift)] < min_pheromone:
                    pheromones[(nurse, day, shift)] = min_pheromone

    # Reinforce pheromones using best solution
    for schedule, _ in population:
        for nurse in nurses:
            for day, shift in enumerate(schedule[nurse]):
                if best_quality > 0:
                    pheromones[(nurse, day, shift)] += 1 / max(best_quality, 1e-6)

    for nurse in nurses:
        for day in range(days):
            for shift in shifts:
                if pheromones[(nurse, day, shift)] > max_pheromone:
                    pheromones[(nurse, day, shift)] = max_pheromone

print("Best schedule:", best_schedule)
print("Best quality:", best_quality)

end = time.time()
print("Execution time (seconds):")
print(end - start)
