from typing import Tuple

Point = Tuple[int, int, int]

cubes = set()
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        cubes.add(tuple(int(v) for v in line.split(",")))


def move_cube(cube: Point, offset: Point) -> Point:
    return (
        cube[0] + offset[0],
        cube[1] + offset[1],
        cube[2] + offset[2],
    )


def mul_vec(point: Point, value: int) -> Point:
    return (point[0] * value, point[1] * value, point[2] * value)


def is_within_bounds(point: Point) -> bool:
    for coordinate in point:
        if not (0 <= coordinate <= 21):
            return False
    return True


def can_reach_outside(point: Point) -> bool:
    visited = set()
    points = [point]
    while points:
        next_point = points.pop()
        if next_point in visited:
            continue
        visited.add(next_point)
        if next_point in cubes:
            continue
        if not is_within_bounds(next_point):
            return True
        for offset in offsets:
            moved = move_cube(next_point, offset)
            if moved not in visited:
                points.append(moved)

    return False


def is_free(point: Point) -> bool:
    if point in point_result:
        return point_result[point]
    free = can_reach_outside(point)
    point_result[point] = free
    return free


point_result = {}
exposed = 0
offsets = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
)
for cube in cubes:
    moved = (move_cube(cube, offset) for offset in offsets)
    exposed += sum(1 if is_free(o) else 0 for o in moved)
    print("moved")

print(exposed)

# 2043 too low
