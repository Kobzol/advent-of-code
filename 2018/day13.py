with open("input.txt", "r") as f:
    lines = [line for line in f]

width = max(len(line) for line in lines)
height = len(lines)

for i, line in enumerate(lines):
    if len(line) < width:
        lines[i] = line + (" " * (width - len(line)))
    lines[i] = list(lines[i])

cars = []
directions = "<^>v"

for y in range(height):
    for x in range(width):
        if lines[y][x] in directions:
            cars.append([[y, x], directions.index(lines[y][x]), 0])  # pos, dir, state
            map = {
                "<": "-",
                ">": "-",
                "^": "|",
                "v": "|"
            }
            lines[y][x] = map[lines[y][x]]


def get(pos):
    return lines[pos[0]][pos[1]]


def hashpos(pos):
    return "{}-{}".format(pos[1], pos[0])


def getdir(c):
    return directions.index(c)


tick = 0
while len(cars) > 1:
    cars = sorted(cars, key=lambda c: c[0])
    toremove = set()
    for car in cars:
        if id(car) in toremove:
            continue

        pos = car[0]
        dir = car[1]
        state = car[2]
        map = {
            0: (0, -1),
            1: (-1, 0),
            2: (0, 1),
            3: (1, 0)
        }
        pos[0] += map[dir][0]
        pos[1] += map[dir][1]

        for c2 in cars:
            if car is c2:
                continue
            if c2[0] == pos:
                toremove.add(id(car))
                toremove.add(id(c2))
                break

        field = get(pos)
        turn = 0
        if field == "+":
            if state == 0:  # turn left
                turn = -1
            elif state == 2:  # turn right
                turn = 1
            state = (state + 1) % 3
        elif field == "/":
            if dir in [getdir("^"), getdir("v")]:
                turn = 1
            else:
                turn = -1
        elif field == "\\":
            if dir in [getdir("^"), getdir("v")]:
                turn = -1
            else:
                turn = 1
        elif field == " ":
            assert False

        car[1] = ((dir + turn) + 4) % 4
        car[2] = state

    cars = [c for c in cars if id(c) not in toremove]
    tick += 1

print(cars, tick)
print(hashpos(cars[0][0]))
