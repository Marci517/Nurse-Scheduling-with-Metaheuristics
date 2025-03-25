import random
import math
import time

n = 2  # number of nurses
d = 5  # number of days

t0 = 100
max_iter = 100


def modified(schedule):
    new_schedule = [s[:] for s in schedule]
    nurse_index = random.randint(0, n - 1)
    day_index = random.randint(0, d - 1)

    new_shift = random.choice([0, 1, 2])
    new_schedule[nurse_index][day_index] = new_shift

    return new_schedule


def quality(schedule):
    soft_constraints = 0
    hard_constraints = 0

    for i in range(n):
        for day in range(d - 1):
            if schedule[i][day] == 2 and schedule[i][day + 1] == 0:
                hard_constraints += 1

    for i in range(n):
        consecutive_work = 0
        for day in range(d):
            if schedule[i][day] != -1:
                consecutive_work += 1
                if consecutive_work > 7:
                    soft_constraints += 1
            else:
                consecutive_work = 0

    return hard_constraints * 100 + soft_constraints * 10


def cooling1(iteration):
    alpha = 1
    tk = t0 / (1 + alpha * iteration)
    return tk


# For faster cooling
def cooling2(it):
    alpha = 0.85
    tk = t0 * alpha ** it
    return tk


def sa(initial_solution):
    t = t0
    current = [s[:] for s in initial_solution]
    best = [s[:] for s in current]

    k = 0
    while t > 0 and k < max_iter:
        new = modified(current)

        r = random.random()
        if quality(new) < quality(current) or r < math.exp((quality(current) - quality(new)) / t):
            current = new.copy()

        if quality(current) < quality(best):
            best = [s[:] for s in current]

        t = cooling2(k)
        k += 1

    return best


POP_SIZE = 20
GENERATIONS = 20
MUTATION_RATE = 0.1


def initialize():
    population = []
    for _ in range(POP_SIZE):
        schedule = []
        for _ in range(n):
            row = [random.choice([0, 1, 2]) for _ in range(d)]
            schedule.append(row)
        population.append(schedule)
    return population


def selection(pop):
    candidates = random.sample(pop, 2)
    candidates.sort(key=lambda x: quality(x))
    return candidates[0]


def crossover(parent1, parent2):
    cut_point = random.randint(1, n - 1)
    child1 = parent1[:cut_point] + parent2[cut_point:]
    child2 = parent2[:cut_point] + parent1[cut_point:]
    return child1, child2


def mutation(solution):
    mutated = [row[:] for row in solution]
    for i in range(n):
        for j in range(d):
            if random.random() < MUTATION_RATE:
                mutated[i][j] = random.choice([0, 1, 2])
    return mutated


def saga():
    population = initialize()

    best = None
    best_quality = float('inf')

    for gen in range(GENERATIONS):
        new_population = []

        population.sort(key=lambda x: quality(x))
        current_best = population[0]
        current_best_quality = quality(current_best)
        if current_best_quality < best_quality:
            best_quality = current_best_quality
            best = [row[:] for row in current_best]

        while len(new_population) < POP_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)

            child1, child2 = crossover(parent1, parent2)

            child1 = mutation(child1)
            child2 = mutation(child2)

            child1 = sa(child1)
            child2 = sa(child2)

            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)

        population = new_population

    return best


start = time.time()
best = saga()

print("Best quality:", quality(best))
print("Best schedule:")
for i in range(n):
    print(f"Nurse {i + 1}: {best[i]}")

end = time.time()

print("Execution time:")
print(end - start)
