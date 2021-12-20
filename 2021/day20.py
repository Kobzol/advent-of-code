from collections import deque
from typing import Dict, Tuple

import tqdm

pixels = {}
row = 0
cols = 0

with open("input.txt") as f:
    enhancement = f.readline().strip()
    f.readline()
    for line in f:
        line = line.strip()
        cols = max(cols, len(line))
        for (index, col) in enumerate(line):
            pixels[(row, index)] = col
        row += 1
bounds = ((0, row), (0, cols))


def neighbours(position: Tuple[int, int]):
    for row in range(-1, 2):
        for col in range(-1, 2):
            yield (position[0] + row, position[1] + col)


Point = Tuple[int, int]


def neighbour_bits(pixels: Dict[Point, str], position: Tuple[int, int], infinite: str):
    for (r, c) in neighbours(position):
        char = pixels.get((r, c), infinite)
        if char == "#":
            yield "1"
        else:
            yield "0"


def step(pixels: Dict[Point, str], bounds: Tuple[Point, Point], infinite: str) -> Dict[Point, str]:
    new_pixels = {}

    for row in range(bounds[0][0], bounds[0][1] + 1):
        for col in range(bounds[1][0], bounds[1][1] + 1):
            pixel = (row, col)
            for neighbour in neighbours(pixel):
                char = enhancement[int("".join(neighbour_bits(pixels, neighbour, infinite)), 2)]
                new_pixels[neighbour] = char
    return new_pixels


chars = deque([".", "#"])
for i in tqdm.tqdm(range(50)):
    infinite = chars[0]
    pixels = step(pixels, bounds, infinite)
    chars.rotate(1)
    bounds = ((bounds[0][0] - 2, bounds[0][1] + 2), (bounds[1][0] - 2, bounds[1][1] + 2))
assert chars[0] == "."
print(sum(1 if v == "#" else 0 for v in pixels.values()))

# 5868 too low
# 5798 too low
