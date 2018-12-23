from collections import deque

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

bots = []

for line in lines:
    pos = list(map(int, line[line.index("pos=<") + 5:line.index(">")].split(",")))
    radius = int(line[line.index("r=") + 2:])
    bots.append((tuple(pos), radius))

bots = sorted(bots, key=lambda b: b[1], reverse=True)


def dist(a, b):
    return sum(abs(x-y) for (x, y) in zip(a, b))


def inrange(pos, bot):
    return dist(pos, bot[0]) <= bot[1]


def botcount(pos):
    return len(list(bot for bot in bots if inrange(pos, bot)))


def gen_moves(pos):
    for dim in range(3):
        for dir in (-1, 0, 1):
            position = list(pos)
            position[dim] = position[dim] + dir
            position = tuple(position)
            if position != pos:
                yield position


best_pos = (0, 0, 0)
best_count = botcount(best_pos)
visited = set()

queue = deque()
queue.append((0, 0, 0))
while queue:
    pos = queue.popleft()
    visited.add(pos)
    count = botcount(pos)
    if count == 0:
        continue
    if count > best_count:
        best_count = count
        best_pos = pos
        print(best_count, best_pos)
    moves = list(gen_moves(pos))
    for move in moves:
        if move not in visited:
            queue.append(move)
