import collections

import networkx

adapters = [0]
with open("input.txt") as f:
    for row in f:
        adapters.append(int(row.strip()))

adapters = sorted(adapters)
adapters.append(adapters[-1] + 3)


def count_connections(adapters, index, visited):
    if index == 0:
        return 1

    if index in visited:
        return visited[index]

    value = adapters[index]
    i = index - 1
    count = 0

    while i >= 0:
        if value - adapters[i] <= 3:
            count += count_connections(adapters, i, visited)
        i -= 1
    visited[index] = count
    return count


print(count_connections(adapters, len(adapters) - 1, {}))
