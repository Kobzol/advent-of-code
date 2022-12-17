import dataclasses
from typing import List, Optional, Set, Tuple

Point = Tuple[int, int]


@dataclasses.dataclass
class Shape:
    points: List[Point]
    pos: Point = (0, 0)
    bottom_offset: int = 0

    def actual_points(self) -> List[Point]:
        return [(self.pos[0] + p[0], self.pos[1] + p[1]) for p in self.points]

    def with_pos(self, pos: Point) -> "Shape":
        return dataclasses.replace(self, pos=pos)

    def is_ok(self, map: Set[Point]) -> bool:
        for point in self.actual_points():
            if point[0] < 0:
                return False
            if not (0 <= point[1] < 7):
                return False
            if point in map:
                return False
        return True


def generate_shapes():
    while True:
        # Horizontal line
        yield Shape([(0, 0), (0, 1), (0, 2), (0, 3)])

        # Cross
        yield Shape([
            (0, 0),
            (0, 1),
            (0, 2),
            (-1, 1),
            (1, 1)
        ], bottom_offset=1)

        # L
        yield Shape([
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2)
        ])

        # Vertical line
        yield Shape([(0, 0), (1, 0), (2, 0), (3, 0)])

        # Square
        yield Shape([
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1)
        ])


def place_shape(map: Set[Point], shape: Shape):
    col = 2
    row = get_max_height(map) + 3 + shape.bottom_offset
    shape.pos = (row, col)


def get_max_height(map: Set[Point]) -> int:
    if not map:
        return 0
    return max((m[0] for m in map)) + 1


@dataclasses.dataclass
class MovementGenerator:
    movements: str
    index: int = 0

    def next(self) -> str:
        dir = self.movements[self.index]
        self.index = (self.index + 1) % len(self.movements)
        return dir


class ShapeGenerator:
    def __init__(self):
        self.gen = generate_shapes()
        self.index = 0

    def next(self) -> Shape:
        shape = next(self.gen)
        self.index = (self.index + 1) % 5
        return shape


def draw_map(map: Set[Point], shape: Optional[Shape] = None):
    if shape is not None:
        map = set(map)
        for p in shape.actual_points():
            map.add(p)

    height = get_max_height(map)
    for row in range(height):
        for col in range(7):
            if (height - (row + 1), col) in map:
                print("#", end="")
            else:
                print(".", end="")
        print()
    input()


def generate_landscape_key(map: Set[Point]):
    key = []
    for col in range(7):
        max_y = max((m[0] for m in map if m[1] == col), default=-1) + 1
        key.append(max_y)

    min_y = min(key)
    key = [y - min_y for y in key]
    return tuple(key)


with open("input.txt") as f:
    movement_gen = MovementGenerator(f.read().strip())

map = set()

shape_gen = ShapeGenerator()
cache = {}

total_steps = 1000000000000
step = 0
total_height = 0
cycle_found = False

while step < total_steps:
    key = (shape_gen.index, movement_gen.index, generate_landscape_key(map))
    # print(key)
    # if not cycle_found:
    if key in cache:
        prev_height, prev_step = cache[key]
        curr_height = get_max_height(map)
        diff_height = curr_height - prev_height
        diff_step = step - prev_step
        print(f"Hit: {key}, diff height: {diff_height}, diff steps: {diff_step}")
        steps_remaining = total_steps - step
        if steps_remaining % diff_step == 0:
            total_height = (steps_remaining // diff_step) * diff_height + curr_height
            print(total_height)
            exit()
            # step = total_steps - (steps_remaining % diff_step)
    else:
        cache[key] = (get_max_height(map), step)

    shape = shape_gen.next()
    place_shape(map, shape)
    # draw_map(map, shape=shape)
    while True:
        dir = movement_gen.next()
        if dir == ">":
            next_shape = shape.with_pos((shape.pos[0], shape.pos[1] + 1))
        elif dir == "<":
            next_shape = shape.with_pos((shape.pos[0], shape.pos[1] - 1))
        else:
            assert False
        if next_shape.is_ok(map):
            shape = next_shape
            # draw_map(map, shape=shape)
        next_shape = shape.with_pos((shape.pos[0] - 1, shape.pos[1]))
        if next_shape.is_ok(map):
            shape = next_shape
            # draw_map(map, shape=shape)
        else:
            assert shape.is_ok(map)
            for point in shape.actual_points():
                map.add(point)
            break
    # draw_map(map)
    step += 1

print(get_max_height(map) + total_height)
