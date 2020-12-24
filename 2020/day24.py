from collections import defaultdict

tile_commands = []


def iterate_commands(path):
    index = 0
    while index < len(path):
        c = path[index]
        if c in ("n", "s"):
            yield path[index:index+2]
            index += 2
        else:
            yield path[index:index+1]
            index += 1


with open("input.txt") as f:
    for line in f:
        line = line.strip()
        tile_commands.append(list(iterate_commands(line)))


def get_location(commands):
    pos = [0, 0]
    for command in commands:
        if "n" in command:
            pos[0] -= 1
        if "s" in command:
            pos[0] += 1
        if "e" in command:
            pos[1] += 2 if command == "e" else 1
        if "w" in command:
            pos[1] -= 2 if command == "w" else 1
    return tuple(pos)


def get_neighbours(pos):
    for command in ("w", "e", "ne", "se", "nw", "sw"):
        location = get_location([command])
        yield (pos[0] + location[0], pos[1] + location[1])


def get_alive_neighbours(state, pos):
    alive = 0
    for neighbour in get_neighbours(pos):
        if state.get(neighbour, False):
            alive += 1
    return alive


def check(pos, state, next_state):
    alive = get_alive_neighbours(state, pos)
    if state.get(pos, False):
        if alive == 0 or alive > 2:
            pass  # set to white
        else:
            next_state[pos] = True
    elif alive == 2:
        next_state[pos] = True


def move(state):
    next_state = {}
    for pos in state:
        check(pos, state, next_state)
        for neighbour in get_neighbours(pos):
            if neighbour not in state:
                check(neighbour, state, next_state)
    return next_state


state = defaultdict(lambda: False)
for command in tile_commands:
    location = get_location(command)
    state[location] = not state[location]

state = dict(state)
for i in range(100):
    state = move(state)

print(len([v for v in state.values() if v]))
