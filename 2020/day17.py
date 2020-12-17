active = set()
with open("input.txt") as f:
    for (row, line) in enumerate(f):
        line = line.strip()
        for (col, point) in enumerate(line):
            if point == "#":
                active.add((row, col, 0, 0))


def iterate_neighbors(pos):
    x, y, z, w = pos
    for x1 in range(-1, 2):
        for y1 in range(-1, 2):
            for z1 in range(-1, 2):
                for w1 in range(-1, 2):
                    position = (x + x1, y + y1, z + z1, w + w1)
                    if pos == position:
                        continue
                    yield position


def count_alive_neighbors(active, pos):
    alive = 0
    for neighbor in iterate_neighbors(pos):
        if neighbor in active:
            alive += 1
    return alive


def check_item(pos, active, next):
    neighbors = count_alive_neighbors(active, pos)
    alive = pos in active

    # print(f"Checking {pos}, was {alive}, has {neighbors} alive neighbors")

    if alive and neighbors in (2, 3):
        next.add(pos)
    elif not alive and neighbors == 3:
        next.add(pos)


def move(active):
    next = set()

    for pos in active:
        check_item(pos, active, next)
        for neighbor in iterate_neighbors(pos):
            if neighbor not in active:
                check_item(neighbor, active, next)

    return next


for _ in range(6):
    active = move(active)

print(len(active))
