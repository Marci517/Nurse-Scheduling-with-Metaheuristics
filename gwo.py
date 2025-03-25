import random
import time

N = 10  # Number of wolves
n = 50  # Number of nurses
d = 10  # Number of days
max_iter = 200
a_init = 2.0  # Initial value of parameter 'a' in GWO


def initialize():
    wolves = []
    for _ in range(N):
        wolf = []
        for _ in range(n):
            wolf.append([random.choice([0, 1, 2]) for __ in range(d)])
        wolves.append(wolf)
    return wolves


def quality(wolf):
    hard_constraints = 0
    soft_constraints = 0
    for i in range(n):
        for day in range(d - 1):
            if wolf[i][day] == 2 and wolf[i][day + 1] == 0:
                hard_constraints += 1

    for i in range(n):
        consecutive_work = 0
        for day in range(d):
            if wolf[i][day] != -1:
                consecutive_work += 1
                if consecutive_work > 7:
                    soft_constraints += 1
            else:
                consecutive_work = 0

    return hard_constraints * 100 + soft_constraints * 10


def update_position(current_wolf, alpha, beta, delta, a):
    new_wolf = []
    for i in range(n):
        new_schedule = []
        for day in range(d):
            r1, r2 = random.random(), random.random()
            A1 = 2 * a * r1 - a
            C1 = 2 * r2

            r3, r4 = random.random(), random.random()
            A2 = 2 * a * r3 - a
            C2 = 2 * r4

            r5, r6 = random.random(), random.random()
            A3 = 2 * a * r5 - a
            C3 = 2 * r6

            D_alpha = abs(C1 * alpha[i][day] - current_wolf[i][day])
            X1 = alpha[i][day] - A1 * D_alpha

            D_beta = abs(C2 * beta[i][day] - current_wolf[i][day])
            X2 = beta[i][day] - A2 * D_beta

            D_delta = abs(C3 * delta[i][day] - current_wolf[i][day])
            X3 = delta[i][day] - A3 * D_delta

            new_X = (X1 + X2 + X3) / 3.0

            rounded_X = round(new_X)
            rounded_X = max(0, min(2, rounded_X))

            new_schedule.append(rounded_X)
        new_wolf.append(new_schedule)
    return new_wolf


def sort_wolves(wolves):
    scored = [(wolf, quality(wolf)) for wolf in wolves]
    scored.sort(key=lambda x: x[1])
    return [x[0] for x in scored], [x[1] for x in scored]


start = time.time()

wolves = initialize()
wolves, quality_values = sort_wolves(wolves)

alpha = wolves[0]
beta = wolves[1]
delta = wolves[2]

a = a_init
t = 0
while t < max_iter:
    for i in range(3, N):
        wolves[i] = update_position(wolves[i], alpha, beta, delta, a)
    wolves, quality_values = sort_wolves(wolves)
    alpha = wolves[0]
    beta = wolves[1]
    delta = wolves[2]
    a = a_init - t * (a_init / max_iter)  # Linear decrease of 'a'
    t += 1

print("Best quality:", quality(alpha))
print("Best schedule:")
for i in range(n):
    print(f"Nurse {i + 1}: {alpha[i]}")

end = time.time()
print("Execution time (seconds):")
print(end - start)
