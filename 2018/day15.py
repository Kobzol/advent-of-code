import copy
import itertools
from collections import deque

with open("input.txt", "r") as f:
    lines = [list(line.strip()) for line in f]

height = len(lines)
width = len(lines[0])

units = []  # [team, hp, attack, [y, x], active]
for y in range(height):
    for x in range(width):
        if lines[y][x] in "GE":
            units.append([lines[y][x], 200, 3, [y, x], True])


def readord(u):
    return sorted(u, key=lambda unit: unit[3])


def is_valid(pos):
    return 0 <= pos[0] < height and 0 <= pos[1] < width


def move(pos, vec):
    return [pos[0] + vec[0], pos[1] + vec[1]]


def get(pos):
    return lines[pos[0]][pos[1]]


def setpos(pos, val):
    lines[pos[0]][pos[1]] = val


moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def select_shortest(start, positions):
    visited = set()
    queue = deque()

    start = tuple(start)
    queue.append(start)
    predecessors = {}
    distances = {}
    distances[start] = 0

    while queue:
        v = queue.popleft()
        if v in visited:
            continue
        visited.add(v)
        for vec in moves:
            target = tuple(move(v, vec))
            if is_valid(target) and get(target) == '.' and target not in visited:
                queue.append(target)
                distances[target] = distances[v] + 1
                predecessors.setdefault(target, []).append(v)

    valid = [tuple(pos) for pos in positions if tuple(pos) in visited]
    if not valid:
        return None
    valid = sorted(valid, key=lambda k: distances[k])
    shortest_dist = distances[valid[0]]
    shortest = [v for v in valid if distances[v] == shortest_dist]
    shortest = sorted(shortest)[0]

    def get_paths(to):
        if to == start:
            return [[to]]
        parents = predecessors[to]
        paths = []
        for p in parents:
            paths += [path + [to] for path in get_paths(p)]
        return paths
    paths = sorted(get_paths(shortest), key=lambda p: p[1])
    return paths[0][1]


def printgrid():
    for y in range(height):
        for x in range(width):
            print(lines[y][x], end="")
        print()


def game(attacks):
    global units

    turn = 0
    while units:
        units = readord(units)
        for i, unit in enumerate(units):
            if not unit[4]:
                continue

            enemies = [u for u in units if u[0] != unit[0] and u[4]]
            if not enemies:
                units = [u for u in units if u[4]]
                return turn
            positions = set(itertools.chain.from_iterable((tuple(move(enemy[3], vec))
                                                           for vec in moves
                                                           if is_valid(move(enemy[3], vec))) for enemy in enemies))
            can_attack = tuple(unit[3]) in positions
            if not can_attack:
                positions = [p for p in positions if get(p) == '.']
                if not positions:
                    continue
                pos = select_shortest(unit[3], positions)
                if pos is None:
                    continue
                assert get(pos) == '.'
                setpos(unit[3], '.')
                setpos(pos, unit[0])
                unit[3] = list(pos)

            adjacents = [move(unit[3], vec) for vec in moves if is_valid(move(unit[3], vec))]
            # attack
            near_enemies = [e for e in enemies if e[3] in adjacents]
            if not near_enemies:
                continue
            target = sorted(near_enemies, key=lambda e: (e[1], e[3]))[0]
            target[1] -= attacks[unit[0]]
            if target[1] <= 0:
                if target[0] == 'E':
                    raise ValueError()
                target[4] = False
                setpos(target[3], '.')

        units = [u for u in units if u[4]]  # remove killed units

        turn += 1
    return turn


attack = 3
orig_lines = copy.deepcopy(lines)
orig_units = copy.deepcopy(units)

while True:
    units = copy.deepcopy(orig_units)
    lines = copy.deepcopy(orig_lines)
    try:
        turns = game({"G": 3, "E": attack})
    except ValueError as e:
        attack += 1
        continue

    hps = sum([u[1] for u in units])
    assert len(set(u[0] for u in units)) == 1
    print(turns, hps, turns * hps)
    break
