from queue import PriorityQueue

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

depth = 11991
target = (797, 6)
erolevels = {}


def erolevel(pos):
    if pos not in erolevels:
        erolevels[pos] = (geoindex(pos) + depth) % 20183

    return erolevels[pos]


def geoindex(pos):
    y, x = pos
    if y == 0 and x == 0:
        return 0
    elif pos == target:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return erolevel((y-1, x)) * erolevel((y, x-1))


def risklevel(pos):
    return erolevel(pos) % 3


def geotype(pos):
    if pos == (0, 0):
        return "M"

    ero = erolevel(pos) % 3
    return {
        0: ".",
        1: "=",
        2: "|"
    }[ero]


def get_tools(pos):
    geo_type = geotype(pos)
    if geo_type == "M":
        return [0, 1, 2]
    elif geo_type == ".":
        return [0, 1]
    elif geo_type == "=":
        return [1, 2]
    elif geo_type == "|":
        return [0, 2]


def dijkstra(start, target):
    visited = set()
    queue = PriorityQueue()
    queue.put((0, start, 0))
    while not queue.empty():
        dist, pos, tool = queue.get()
        if (pos, tool) == (target, 0):
            return dist
        if (pos, tool) in visited:
            continue
        visited.add((pos, tool))
        tools = get_tools(pos)
        for t in tools:
            if t != tool:
                queue.put((dist + 7, pos, t))
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for move in moves:
            target_pos = (move[0] + pos[0], move[1] + pos[1])
            if target_pos[0] < 0 or target_pos[1] < 0:
                continue
            if tool in get_tools(target_pos):
                queue.put((dist + 1, target_pos, tool))

print(dijkstra((0, 0), target))
