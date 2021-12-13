import numpy as np

points = []
folds = []

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            break
        x, y = line.strip().split(",")
        points.append((int(x), int(y)))

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    for line in f:
        folds.append(line.strip())
# x -> right
# y -> down
# (x, y)

map = np.zeros((max_y + 1, max_x + 1), dtype=int)
for (col, row) in points:
    map[row, col] = 1

for fold in folds:
    axis, value = fold[len("fold along "):].split("=")
    value = int(value)
    rows, cols = map.shape
    if axis == "y":
        map[:value, :] |= np.flip(map[value + 1:, :], axis=0)
        map = map[:value, :]
    elif axis == "x":
        map[:, :value] |= np.flip(map[:, value + 1:], axis=1)
        map = map[:, :value]

for row in range(map.shape[0]):
    for col in range(map.shape[1]):
        print("#" if map[row, col] else " ", end="")
    print()
