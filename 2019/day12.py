import re
import itertools

import numpy as np

regex = re.compile(r".*?=(-?\d+).*?=(-?\d+).*?=(-?\d+).*?")
moons = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        res = regex.match(line)
        moons.append([[int(res.group(i)) for i in range(1, 4)], [0] * 3])

moons = np.array(moons)


def potential_energy(moon):
    return np.sum(np.abs(moon[0]))


def kinetic_energy(moon):
    return np.sum(np.abs(moon[1]))


def energy(moon):
    return potential_energy(moon) * kinetic_energy(moon)


states = [{} for i in range(3)]
steps = 0
periods = {}
found = [False for i in range(3)]

while True:
    for i in range(3):
        hash = ";".join(str(x) for x in moons[:, :, i].ravel())

        if hash in states[i] and not found[i]:
            print(i, steps)
            found[i] = True
        states[i][hash] = steps
    steps += 1
    for (moon, other) in itertools.combinations(moons, 2):
        offset = other[0] - moon[0]
        offset = np.sign(offset)
        moon[1] += offset
        other[1] += (offset * -1)
    for moon in moons:
        moon[0] += moon[1]

# 24072078 too high
