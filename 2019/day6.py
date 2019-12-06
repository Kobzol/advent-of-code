import networkx
from networkx import shortest_path_length

g = networkx.DiGraph()

with open("input.txt") as f:
    for line in f:
        dst, src = line.strip().split(")")
        g.add_edge(src, dst)

"""routes = 0
for node in g.nodes:
    for other in g.nodes:
        if node == other:
            continue
        if has_path(g, node, other):
            routes += 1
print(routes)"""

start = list(g.neighbors("YOU"))[0]
end = list(g.neighbors("SAN"))[0]


def length(node):
    lengths = shortest_path_length(g, node)
    if start not in lengths or end not in lengths:
        return 10e10
    return lengths[start] + lengths[end]


g = g.reverse()
s = [length(node) for node in g.nodes]
print(min(s))
