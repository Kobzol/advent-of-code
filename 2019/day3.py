def get_positions(moves):
    pos = (0, 0)
    positions = set()
    counts = {}

    offsets = {
        "U": (0, -1),
        "R": (1, 0),
        "D": (0, 1),
        "L": (-1, 0)
    }

    counter = 0
    for move in moves:
        count = int(move[1:])
        dir = move[0]
        for i in range(count):
            pos = (pos[0] + offsets[dir][0], pos[1] + offsets[dir][1])
            positions.add(pos)
            counter += 1
            if pos not in counts:
                counts[pos] = counter

    return positions, counts


def manhattan(a, b=(0, 0)):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


wires = []

with open("input.txt") as f:
    for wire in f:
        moves = wire.strip().split(",")
        wires.append(get_positions(moves))

union = wires[0][0] & wires[1][0]
s = sorted(union, key=lambda p: wires[0][1][p] + wires[1][1][p])
p = s[0]
print(p, wires[0][1][p] + wires[1][1][p])
