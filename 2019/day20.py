import networkx
from networkx import shortest_path

grid = []
maxline = 0
with open("input.txt") as f:
    for line in f:
        grid.append(list(line[:-1]))
        maxline = max(maxline, len(line) - 1)

for line in grid:
    line.extend([' '] * (maxline - len(line)))


def is_valid(row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[row])


def is_outer(position, dir):
    while True:
        position = (position[0] + dir[0], position[1] + dir[1])
        if not is_valid(*position):
            return True
        else:
            ch = grid[position[0]][position[1]]
            if ch.isupper() or ch in (".", "#"):
                return False


outer_portals = {}
inner_portals = {}
graph = networkx.Graph()

for i, row in enumerate(grid):
    for j, col in enumerate(row):
        dirs = (
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        )

        if col == '.':
            for (x, y) in dirs:
                px = x + i
                py = y + j
                if is_valid(px, py):
                    if grid[px][py] == '.':
                        graph.add_edge(((i, j), 0), ((px, py), 0))
                    elif grid[px][py].isupper():
                        ch1 = grid[px][py]
                        ch2 = grid[px + x][py + y]
                        assert ch2.isupper()
                        label = "{}{}".format(ch1, ch2)
                        if (x, y) in ((-1, 0), (0, -1)):
                            label = label[::-1]
                        if is_outer((px + x, py + y), (x, y)):
                            outer_portals[label] = (i, j)
                        else:
                            inner_portals[label] = (i, j)

for key in inner_portals:
    assert key in outer_portals


edges = set()
for ((src, _), (dst, _)) in graph.edges:
    edges.add((src, dst))


def unroll(graph, level):
    for (src, dst) in edges:
        graph.add_edge((src, level), (dst, level))
    for key in inner_portals:
        graph.add_edge((inner_portals[key], level - 1), (outer_portals[key], level))


level = 1
while True:
    print(level)
    try:
        s = shortest_path(graph, source=(outer_portals["AA"], 0), target=(outer_portals["ZZ"], 0))
        print(len(s) - 1, s)
        break
    except networkx.NetworkXNoPath:
        unroll(graph, level)
        level += 1
