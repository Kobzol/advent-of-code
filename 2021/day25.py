map = []

with open("input.txt") as f:
    for line in f:
        map.append(list(line.strip()))


rows = len(map)
cols = len(map[0])


def move(map) -> bool:
    next_map = [list(c) for c in map]
    move = False

    for row in range(rows):
        for col in range(cols):
            item = map[row][col]
            if item == ">":
                right = (col + 1) % cols
                if map[row][right] == ".":
                    next_map[row][right] = ">"
                    next_map[row][col] = "."
                    move = True

    map = next_map
    next_map = [list(c) for c in map]

    for row in range(rows):
        for col in range(cols):
            item = map[row][col]
            if item == "v":
                down = (row + 1) % rows
                if map[down][col] == ".":
                    next_map[down][col] = "v"
                    next_map[row][col] = "."
                    move = True

    return (move, next_map)


def print_map(map):
    for row in map:
        print("".join(row))
    print()


step = 0
while True:
    moved, map = move(map)
    step += 1
    # if step == 58:
    #     print_map(map)
    if not moved:
        break
print(step)
