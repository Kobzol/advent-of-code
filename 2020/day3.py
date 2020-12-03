import re
import itertools

regex = re.compile(r"(\d+)-(\d+) (\w): (.*)")

valid = 0

map = []
with open("input.txt") as f:
    for row in f:
        line = row.strip()
        map.append(line)

def check(move):
    pos = [0, 0]
    valid = 0
    while True:
        if map[pos[0]][pos[1] % len(map[0])] == '#':
            valid += 1
        pos[0] += move[1]
        pos[1] += move[0]
        if pos[0] >= len(map):
            break
    return valid

items = [check([x, y]) for (x, y) in [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]]

i = 1
for j in items:
    i *= j
print(i)
