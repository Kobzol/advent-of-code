import networkx
import numpy as np
from networkx import DiGraph

map = []
with open("input.txt") as f:
    for line in f:
        map.append([int(v) for v in line.strip()])

map = np.array(map, dtype=int)
orig_rows, orig_cols = map.shape

target_map = np.zeros((orig_rows * 5, orig_cols * 5), dtype=int)
rows, cols = target_map.shape

for row in range(5):
    for col in range(5):
        scaled = map + (row + col)
        scaled[scaled > 9] -= 9
        target_map[row * orig_rows:(row + 1) * orig_rows,
        col * orig_cols:(col + 1) * orig_cols] = scaled

target_map = target_map % 10
print(target_map)


def is_valid(row: int, col: int) -> bool:
    return 0 <= row < rows and 0 <= col < cols


def get_neighbours(row: int, col: int):
    offsets = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for (rowx, colx) in offsets:
        rx = row + rowx
        cx = col + colx
        if is_valid(rx, cx):
            yield (rx, cx)


graph = DiGraph()
for row in range(rows):
    for col in range(cols):
        position = (row, col)
        for (r, c) in get_neighbours(row, col):
            graph.add_edge(position, (r, c), weight=target_map[r][c])

start = (0, 0)
end = (rows - 1, cols - 1)
path = networkx.shortest_path(graph, start, end, weight="weight")
print(path)
cost = sum(target_map[r][c] for (r, c) in path[1:])
print(cost)
