import collections
from typing import List, Optional, Set, Tuple

Point = Tuple[int, int]

elves: Set[Point] = set()
with open("input.txt") as f:
    for (row, line) in enumerate(f):
        line = line.rstrip()
        for (col, value) in enumerate(line):
            if value == "#":
                elves.add((row, col))

NORTH = "N"
SOUTH = "S"
WEST = "W"
EAST = "E"


def generate_directions():
    directions = collections.deque((NORTH, SOUTH, WEST, EAST))
    while True:
        yield tuple(directions)
        directions.rotate(-1)


def get_bbox_size(items: Set[Point]) -> int:
    start_row = min(i[0] for i in items)
    end_row = max(i[0] for i in items)
    start_col = min(i[1] for i in items)
    end_col = max(i[1] for i in items)

    height = (end_row - start_row) + 1
    width = (end_col - start_col) + 1
    return width * height


def get_neighbours(position: Point, dir: Optional[str] = None):
    if dir is None:
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                if (row, col) == (0, 0):
                    continue
                yield (position[0] + row, position[1] + col)
    else:
        offsets = {
            NORTH: ((-1, 0), (-1, 1), (-1, -1)),
            SOUTH: ((1, 0), (1, 1), (1, -1)),
            WEST: ((0, -1), (1, -1), (-1, -1)),
            EAST: ((0, 1), (1, 1), (-1, 1)),
        }
        for (row, col) in offsets[dir]:
            yield (position[0] + row, position[1] + col)


def move_in_dir(position: Point, dir: str) -> Point:
    offsets = {
        NORTH: (-1, 0),
        SOUTH: (1, 0),
        WEST: (0, -1),
        EAST: (0, 1),
    }
    (row, col) = offsets[dir]
    return (position[0] + row, position[1] + col)


def print_items(items: Set[Point]):
    start_row = min(i[0] for i in items)
    end_row = max(i[0] for i in items)
    start_col = min(i[1] for i in items)
    end_col = max(i[1] for i in items)

    height = (end_row - start_row) + 1
    width = (end_col - start_col) + 1

    for row in range(height):
        for col in range(width):
            pos = (row + start_row, col + start_col)
            if pos in items:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def simulate_step(items: Set[Point], dirs: List[str]) -> Set[Point]:
    proposed = collections.defaultdict(int)
    to_move = dict()
    next_items = set()

    for item in items:
        # No neighbours
        if all(neighbor not in items for neighbor in get_neighbours(item)):
            next_items.add(item)
            continue
        added_dir = False
        for dir in dirs:
            if all(neighbor not in items for neighbor in get_neighbours(item, dir=dir)):
                target = move_in_dir(item, dir)
                proposed[target] += 1
                to_move[item] = target
                added_dir = True
                break
        if not added_dir:
            next_items.add(item)

    for (source, target) in to_move.items():
        if proposed[target] == 1:
            next_items.add(target)
        else:
            next_items.add(source)
    assert len(items) == len(next_items)
    return next_items


dir_iter = generate_directions()
round = 0
while True:
    dirs = next(dir_iter)
    next_elves = simulate_step(elves, dirs)
    if elves == next_elves:
        print(round + 1)
        break
    elves = next_elves
    round += 1
