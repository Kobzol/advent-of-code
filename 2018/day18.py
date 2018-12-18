import copy
import sys
from collections import Counter

with open("input.txt", "r") as f:
    lines = [list(line.strip()) for line in f]

height = len(lines)
width = len(lines[0])


def printgrid(f=sys.stdout):
    for i in range(height):
        print("".join(lines[i]), file=f)
    print(file=f)


def tostr():
    str = ""
    for i in range(height):
        str += "".join(lines[i]) + "\n"
    return str


hash = Counter()
lastseen = {}

for index in range(1000000000):
    if index % 100 == 0:
        string = tostr()
        hash[string] += 1
        if len(hash) == 12:
            diff = index - lastseen.get(string, index)
            if diff > 0:
                x = (1000000000 - index) % diff
                if x == 0:
                    print(index, diff, string)
                    exit()
        lastseen[string] = index
        print(index, len(hash))

    next = copy.deepcopy(lines)
    for i in range(height):
        for j in range(width):
            counts = {}
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if k == 0 and l == 0:
                        continue
                    y = i + k
                    x = j + l
                    if 0 <= y < height and 0 <= x < width:
                        counts[lines[y][x]] = counts.get(lines[y][x], 0) + 1
            c = lines[i][j]
            if c == '.':
                if counts.get('|', 0) >= 3:
                    next[i][j] = '|'
            elif c == '|':
                if counts.get('#', 0) >= 3:
                    next[i][j] = '#'
            else:
                if not (counts.get('#', 0) >= 1 and counts.get('|', 0) >= 1):
                    next[i][j] = '.'
    lines = next

counts = Counter()
for i in range(height):
    for j in range(width):
        counts[lines[i][j]] += 1
print(counts)
print(counts['#'] * counts['|'])
