import numpy as np
from numpy import product

map = []
with open("input.txt") as f:
    for line in f:
        line = [int(v) for v in line.strip()]
        map.append(line)


map = np.array(map)
height = map.shape[0]
width = map.shape[1]
visited = np.zeros_like(map, dtype=bool)


def is_valid(row: int, col: int) -> bool:
    return 0 <= row < height and 0 <= col < width


def get_neighbours(row: int, col: int):
    offsets = (
        (-1, 0),
        (1, 0),
        (0, 1),
        (0, -1)
    )
    for (row_dx, col_dx) in offsets:
        r = row + row_dx
        c = col + col_dx
        if is_valid(r, c):
            yield (r, c)


def get_basin_size(row: int, col: int) -> int:
    if not is_valid(row, col) or visited[row, col]:
        return 0
    visited[row, col] = True
    if map[row, col] == 9:
        return 0
    return 1 + sum(get_basin_size(r, c) for (r, c) in get_neighbours(row, col))


basin_sizes = []
for row in range(height):
    for col in range(width):
        basin_sizes.append(get_basin_size(row, col))

basin_sizes = sorted(basin_sizes, reverse=True)[:3]
print(product(basin_sizes))
