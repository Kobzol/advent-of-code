import itertools

import networkx
from networkx import shortest_path, has_path, all_simple_paths

grid = []

with open("input.txt") as f:
    for line in f:
        grid.append(line.strip())

keys = {}
keys_inv = {}
doors = {}
doors_inv = {}
starts = []
graph = networkx.Graph()
neighbours = (
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
)


def is_valid(row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[row])


def connect_door(graph, position):
    for (x, y) in neighbours:
        tx = position[0] + x
        ty = position[1] + y
        if is_valid(tx, ty) and grid[tx][ty] != '#':
            graph.add_edge(position, (tx, ty))


def remove_door(graph, position):
    graph.remove_node(position)


for i, row in enumerate(grid):
    for j, col in enumerate(row):
        if col != '#':
            position = (i, j)
            if col == "@":
                starts.append(position)
            elif col.islower():
                keys[col] = position
                keys_inv[position] = col
            elif col.isupper():
                doors[col] = position
                doors_inv[position] = col
                continue

            for (x, y) in neighbours:
                tx = i + x
                ty = j + y
                if is_valid(tx, ty) and grid[tx][ty] != '#' and not grid[tx][ty].isupper():
                    graph.add_edge(position, (tx, ty))

print(keys)
print(doors)
print(starts)

min_steps = 10e10


def hash_state(positions, remaining_keys):
    state = []
    state += positions
    state += tuple(itertools.chain.from_iterable((sorted(k)) for k in remaining_keys))
    return tuple(state)


def assign(graph, positions, steps, remaining_keys, collected_keys, shortest_paths, cache):
    global min_steps

    step_count = sum(steps)
    if step_count >= min_steps:
        return

    state = hash_state(positions, remaining_keys)
    if cache.get(state, 10e10) <= step_count:
        return
    cache[state] = step_count
    if len(collected_keys) == len(keys):
        min_steps = min(min_steps, step_count)
        print(min_steps)
        return

    for i, position in enumerate(positions):
        reachable_keys = set()
        for key in remaining_keys[i]:
            if len(shortest_paths[(position, key)]["reqs"] - collected_keys) == 0:
                reachable_keys.add(key)

        dists = list((key, shortest_paths[(position, key)]["distance"]) for key in reachable_keys)
        dists.sort(key=lambda k: k[1])

        for (key, distance) in dists:
            new_steps = list(steps)
            new_steps[i] += distance
            new_keys = [set(k) for k in remaining_keys]
            new_keys[i].remove(key)
            new_positions = list(positions)
            new_positions[i] = keys[key]
            new_collected = set(collected_keys)
            new_collected.add(key)
            assign(graph, new_positions, new_steps, new_keys, new_collected, shortest_paths, cache)


for door in doors:
    connect_door(graph, doors[door])
shortest_paths = {}
for key in set(keys.values()) | set(starts):
    for other in set(keys.values()) | set(starts):
        if key == other:
            continue
        try:
            path = shortest_path(graph, source=key, target=other)
            req_doors = set(doors_inv[p].lower() for p in path if p in doors_inv)
            if other not in starts:
                other = keys_inv[other]
            shortest_paths[(key, other)] = {
                "distance": len(path) - 1,
                "reqs": req_doors
            }
        except:
            pass

remaining_keys = []
for pos in starts:
    targets = set()
    for key in keys:
        if has_path(graph, source=pos, target=keys[key]):
            targets.add(key)
    remaining_keys.append(targets)

for door in doors:
    remove_door(graph, doors[door])

assign(graph, starts, [0 for _ in starts], remaining_keys, set(), shortest_paths, {})
print(min_steps)

# 4806 too high
# 3446 too low
