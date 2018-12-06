import numpy as np

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

pole = np.zeros((400, 400))

points = {}

i = 0
for line in lines:
    data = [int(f) for f in line.split(",")]
    pole[data[0], data[1]] = i
    points[i] = (data[0], data[1])
    i += 1

count = 0
for i in range(pole.shape[0]):
    for j in range(pole.shape[1]):
        sum = 0
        for p in points:
            point = points[p]
            sum += abs(i - point[0]) + abs(j - point[1])
        if sum < 10000:
            count += 1

print(count)
for i in range(pole.shape[0]):
    for j in range(pole.shape[1]):
        min_dist = 10e10
        target = None
        more = False
        for p in points:
            point = points[p]
            if point == (i, j):
                target = None
                break
            dist = abs(i - point[0]) + abs(j - point[1])
            if dist < min_dist:
                min_dist = dist
                target = p
                more = False
            elif dist == min_dist:
                more = True
        if target is not None:
            if more:
                pole[i, j] = -1
            else:
                pole[i, j] = target
counts = {}
invalid = {}
for i in range(pole.shape[0]):
    for j in range(pole.shape[1]):
        if pole[i, j] != -1:
            counts[pole[i, j]] = counts.get(pole[i, j], 0) + 1
            if i == 0 or j == 0 or i == pole.shape[0] - 1 or j == pole.shape[1] - 1:
                invalid[pole[i, j]] = True

print(max([counts[val] for val in counts if val not in invalid]))
