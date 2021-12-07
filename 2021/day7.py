import numpy as np
import pandas as pd

with open("input.txt") as f:
    positions = np.array([int(v) for v in f.read().split(",")])


def series_sum(n: int) -> int:
    return int(n * (n + 1) / 2)


def evaluate_cost(positions: np.ndarray, cost: int) -> int:
    distances = np.abs(positions - cost)
    costs = [series_sum(n) for n in distances]
    return int(np.sum(costs))



items = []
maximum = positions.max() * 2
for i in range(-maximum, maximum + 1):
    items.append((i, evaluate_cost(positions, i)))

items = sorted(items, key=lambda v: v[1])
print(items[0])
