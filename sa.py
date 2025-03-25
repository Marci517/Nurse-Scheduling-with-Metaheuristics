import random
import math
import time

n = 10  # number of nurses
d = 20  # number of days

t0 = 1000000
max_iter = 2000

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


# Fast cooling
def cooling2(it):
    alpha = 0.85
    tk = t0 * alpha ** it
    return tk


start = time.time()
t = t0
current = []
for i in range(n):
    row = [random.choice([0, 1, 2]) for _ in range(d)]
    current.append(row)

best = [s[:] for s in current]

k = 0
while t > 0 and k < max_iter:
    new = modified(current)

    r = random.random()
    if quality(new) < quality(current) or r < math.exp((quality(current) - quality(new)) / t):
        current = new.copy()

    if quality(current) < quality(best):
        best = [s[:] for s in current]

    t = cooling1(k)
    k += 1

print("Best quality:", quality(best))
print("Best schedule:")
for i in range(n):
    print(f"Nurse {i + 1}: {best[i]}")

end = time.time()

print("Execution time:")
print(end - start)
