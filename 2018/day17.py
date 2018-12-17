import sys
from collections import deque

import numpy as np

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

grid = np.zeros((2100, 2100), dtype=np.int8)
minY = grid.shape[0]
maxY = 0
minX = grid.shape[1]
maxX = 0

# 0 .
# 1 #
# 2 ~
# 3 |

for line in lines:
    first = int(line[2:line.index(",")])
    first = [first, first]
    second = list(map(int, line[line.index(", ") + 4:].split("..")))
    if line[0] == "x":
        x = second
        second = first
        first = x

    minY = min(minY, *first)
    maxY = max(maxY, *first)
    minX = min(minX, *second)
    maxX = max(maxX, *second)
    grid[first[0]:first[1] + 1, second[0]:second[1] + 1] = 1

minX -= 1
maxX -= 1

print(minY, maxY, minX, maxX)


def get(pos):
    return grid[pos[0], pos[1]]


def printgrid(f=sys.stdout):
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            chars = {
                0: '.',
                1: '#',
                2: '~',
                3: '|'
            }
            f.write(chars[get((y, x))])
        f.write("\n")
    f.write("\n")


def is_filled(pos):
    return get(pos) in (1, 2)


def setval(pos, val):
    grid[pos[0], pos[1]] = val


def is_valid(pos):
    return pos[0] <= maxY


def find_corner(pos, dir):
    if get(pos) == 1:
        return (True, (pos[0], pos[1] - dir))
    else:
        #assert get(pos) in (0, 3)
        bot = (pos[0] + 1, pos[1])
        if get(bot) in (0, 3):
            return (False, pos)
        #assert is_filled(bot)
        return find_corner((pos[0], pos[1] + dir), dir)


next = deque([(0, 500)])


def crawl(pos):
    if get(pos) == 2:
        return
    #assert get(pos) in (0, 3)

    while True:
        setval(pos, 3)
        bot = (pos[0] + 1, pos[1])
        if is_valid(bot) and get(bot) == 0:
            pos = bot
        else:
            break
    if not is_valid(bot):
        return
    if get(bot) == 3:
        return
    #assert get(pos) in (0, 3)

    lc, lpos = find_corner(pos, -1)
    rc, rpos = find_corner(pos, 1)

    if lc and rc:
        grid[pos[0], lpos[1]:rpos[1] + 1] = 2
        crawl((pos[0] - 1, pos[1]))
    else:
        grid[pos[0], lpos[1]:rpos[1] + 1] = 3
        if not lc:
            #assert get(lpos) in (0, 3)
            next.append(lpos)
        if not rc:
            #assert get(rpos) in (0, 3)
            next.append(rpos)


sys.setrecursionlimit(50000)

while next:
    crawl(next.popleft())
grid[0, 500] = 0

count = 0
for y in range(minY, maxY + 1):
    for x in range(minX, maxX + 1):
        if get((y, x)) == 2:
            count += 1
print(count)
