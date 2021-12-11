import numpy as np

lines = []
with open("input.txt") as f:
    for line in f:
        lines.append([int(v) for v in line.strip()])


map = np.array(lines)


def is_valid(row: int, col: int) -> bool:
    return 0 <= row < map.shape[0] and 0 <= col < map.shape[1]


def get_neighbours(row: int, col: int):
    for rx in (-1, 0, 1):
        for cx in (-1, 0, 1):
            if (rx, cx) == (0, 0):
                continue
            r = row + rx
            c = col + cx
            if is_valid(r, c):
                yield (r, c)


def simulate(map: np.ndarray):
    flashes = 0

    map += 1
    visited = np.zeros_like(map, dtype=bool)

    while True:
        cond = np.logical_and(map > 9, visited == False)
        to_flash = cond.nonzero()
        if not len(to_flash[0]):
            break

        for index in range(len(to_flash[0])):
            row, col = (to_flash[0][index], to_flash[1][index])
            assert not visited[row, col]
            visited[row, col] = True
            if not map[row, col] > 9:
                assert False
            map[row, col] = 0
            flashes += 1
            for (r, c) in get_neighbours(row, col):
                if not visited[r, c]:
                    map[r, c] += 1

    return flashes == map.shape[0] * map.shape[1]


step = 0
while True:
    step += 1
    if simulate(map):
        print(step)
        break
