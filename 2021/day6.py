from collections import deque

import numpy as np
from numba.cuda import jit

with open("input.txt") as f:
    data = [int(v) for v in f.read().split(",")]

fishes = np.array(data)


@jit(nopython=True)
def simulate_step(f: np.ndarray) -> np.ndarray:
    new = f[f == 0].size
    f[f == 0] = 7
    f -= 1
    return np.concatenate((f, np.full(new, 8)))


@jit(nopython=True)
def calculate(fishes: np.ndarray) -> int:
    for i in range(256):
        fishes = simulate_step(fishes)
    return fishes.size


def simulate(buffer: deque):
    to_spawn = buffer[0]
    buffer.popleft()
    buffer.append(to_spawn)
    buffer[6] += to_spawn


buffer = deque([0] * 9)
for fish in fishes:
    buffer[fish] += 1

for i in range(256):
    simulate(buffer)

print(sum(buffer))
