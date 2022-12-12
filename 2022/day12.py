import networkx

graph = networkx.DiGraph()

lines = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        lines.append(line)


start = None
end = None
rows = len(lines)
cols = len(lines[0])
dirs = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1)
]


def normalize(item: str) -> str:
    if item == "S":
        return "a"
    if item == "E":
        return "z"
    return item


def distance(source: str, target: str) -> int:
    source = normalize(source)
    target = normalize(target)

    source = ord(source)
    target = ord(target)
    return target - source


for row in range(rows):
    for col in range(cols):
        item = lines[row][col]
        if item == "S":
            start = (row, col)
        elif item == "E":
            end = (row, col)
        for dir in dirs:
            r = row + dir[0]
            c = col + dir[1]
            if 0 <= r < rows and 0 <= c < cols and distance(item, lines[r][c]) <= 1:
                graph.add_edge((row, col), (r, c))

min_dist = None
for row in range(rows):
    for col in range(cols):
        item = lines[row][col]
        if item in ("a", "S"):
            try:
                path = networkx.shortest_path(graph, (row, col), end)
                if min_dist is None or min_dist > len(path):
                    min_dist = len(path)
            except networkx.NetworkXNoPath:
                pass
print(min_dist - 1)
