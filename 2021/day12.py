from collections import defaultdict
from typing import List, Set

graph = defaultdict(set)

with open("input.txt") as f:
    for line in f:
        src, dst = line.strip().split("-")
        graph[src].add(dst)
        graph[dst].add(src)

"""
    start
    /   \
c--A-----b--d
    \   /
     end
"""

paths = set()


def count_paths(start: str, end: str, visited: Set[str], small_visited: Set[str], path: List[str]):
    if start == end:
        paths.add(tuple(path + [end]))
        return 1

    v = set(visited)
    count = 0
    if not start.isupper():
        if start not in ("start", "end") and not small_visited:
            for neighbour in graph[start]:
                if neighbour not in v:
                    count += count_paths(neighbour, end, v, small_visited.union({start}), path + [start])
        v.add(start)

    for neighbour in graph[start]:
        if neighbour not in v:
            count += count_paths(neighbour, end, v, small_visited, path + [start])

    return count


print(count_paths("start", "end", set(), set(), []))
print(len(paths))
