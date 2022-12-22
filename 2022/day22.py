import dataclasses
from typing import Dict, List, Optional, Tuple, Union

Point = Tuple[int, int]
Movement = Union[str, int]


@dataclasses.dataclass
class Location:
    point: Point
    value: str
    face: int = 0
    connections: Dict[Point, "Location"] = dataclasses.field(default_factory=dict)
    face_point: Optional[Point] = None

    def __repr__(self):
        return f"Location(f={self.face}, rel={self.face_point}, abs={self.point}, {self.value})"


@dataclasses.dataclass
class Player:
    point: Location
    dir: Point


def parse_movements(line: str) -> List[Movement]:
    movements = []
    val = None
    for c in line:
        if c.isdigit():
            if val is None:
                val = 0
            else:
                val *= 10
            val += int(c)
        else:
            if val is not None:
                movements.append(val)
                val = None
            movements.append(c)
    if val is not None:
        movements.append(val)

    return movements


def print_face_map(map):
    for row in map:
        for col in row:
            if col is None:
                print(" ", end="")
            else:
                print(col.face, end="")
        print()


def get_facing(player: Player) -> int:
    return {
        (0, 1): 0,
        (-1, 0): 1,
        (0, -1): 2,
        (1, 0): 3
    }[player.dir]


def get_edge(face_index: int, side: str, reverse: bool = False) -> List[Location]:
    assert side in "rblt"
    face = faces[face_index]
    entries = {
        "r": ((0, DIMENSION - 1), (1, 0)),
        "b": ((DIMENSION - 1, 0), (0, 1)),
        "l": ((0, 0), (1, 0)),
        "t": ((0, 0), (0, 1))
    }
    (start, dir) = entries[side]
    items = []
    for _ in range(DIMENSION):
        (row, col) = start
        items.append(face[row * DIMENSION + col])
        start = (start[0] + dir[0], start[1] + dir[1])
    if reverse:
        return items[::-1]
    return items


def connect(
        a_face: int,
        a_side: str,
        b_face: int,
        b_side: str,
        reverse: bool = False
):
    dir_map = {
        "r": RIGHT,
        "b": DOWN,
        "l": LEFT,
        "t": UP
    }
    dir_a = dir_map[a_side]
    dir_b = dir_map[b_side]

    a = get_edge(a_face, a_side, reverse=reverse)
    b = get_edge(b_face, b_side)
    assert len(a) == len(b)
    assert len(a) == DIMENSION
    for (loc_a, loc_b) in zip(a, b):
        assert dir_a not in loc_a.connections
        loc_a.connections[dir_a] = loc_b
        assert dir_b not in loc_b.connections
        loc_b.connections[dir_b] = loc_a

    change = (dir_a, dir_b)
    if change in ((UP, DOWN), (DOWN, UP), (LEFT, RIGHT), (RIGHT, LEFT)):
        face_dir_change[(a_face, b_face)] = None
        face_dir_change[(b_face, a_face)] = None
    elif change in ((LEFT, UP), (UP, RIGHT), (RIGHT, DOWN), (DOWN, LEFT)):
        face_dir_change[(a_face, b_face)] = LEFT
        face_dir_change[(b_face, a_face)] = RIGHT
    elif change in ((LEFT, DOWN), (DOWN, RIGHT), (RIGHT, UP), (UP, LEFT)):
        face_dir_change[(a_face, b_face)] = RIGHT
        face_dir_change[(b_face, a_face)] = LEFT
    else:
        assert change[0] == change[1]
        face_dir_change[(a_face, b_face)] = REVERT
        face_dir_change[(b_face, a_face)] = REVERT


def apply_dir(dir_orig: Point, dir: Point) -> Point:
    (a, b) = dir_orig
    if dir == REVERT:
        return (-a, -b)
    elif dir == RIGHT:
        return (-b, a)
    elif dir == LEFT:
        return (b, -a)
    else:
        assert False


def perform_movement(movement: Movement, player: Player):
    def mark_player():
        mark = {
            RIGHT: ">",
            DOWN: "v",
            LEFT: "<",
            UP: "^"
        }
        steps[player.point.point] = mark[player.dir]
        # draw_map()

    if isinstance(movement, int):
        mark_player()
        for _ in range(movement):
            location = player.point
            next_location = location.connections[player.dir]
            if next_location.value == "#":
                break
            else:
                if location.face != next_location.face:
                    # Change direction
                    dir_change = face_dir_change[(location.face, next_location.face)]
                    if dir_change is not None:
                        player.dir = apply_dir(player.dir, dir_change)
                player.point = next_location
                mark_player()
    elif movement == "L":
        player.dir = apply_dir(player.dir, LEFT)
    elif movement == "R":
        player.dir = apply_dir(player.dir, RIGHT)
    else:
        assert False


# Example input
# DIMENSION = 4
# FACES_ROWWISE = [5, 2, 3, 0, 4, 1]
DIMENSION = 50
FACES_ROWWISE = [5, 1, 0, 3, 4, 2]
RIGHT = (0, 1)
DOWN = (-1, 0)
LEFT = (0, -1)
UP = (1, 0)
REVERT = (1, 1)

map = []
bounds_col = []
max_row_length = 0
with open("input.txt") as f:
    for line in f:
        line = line.rstrip()
        if not line:
            break
        start = 0
        for index in range(len(line)):
            if line[index] != " ":
                break
            start += 1

        row = len(map)
        columns = []
        for (index, c) in enumerate(line[start:]):
            column = start + index
            columns.append(Location(point=(row, column), value=c))

        row_length = start + len(columns)
        max_row_length = max(max_row_length, row_length)
        bounds_col.append((start, row_length - 1))
        map.append(columns)

    for line in f:
        movements = parse_movements(line.strip())
        break

bounds_row = []
for column in range(max_row_length):
    start = min(index for (index, row) in enumerate(map) if column in (loc.point[1] for loc in row))
    end = max(index for (index, row) in enumerate(map) if column in (loc.point[1] for loc in row))
    bounds_row.append((start, end))

# Make map dense
dense_map = []
for row in map:
    start = row[0].point[1]
    end = row[-1].point[1]
    remaining_end = max_row_length - (end + 1)

    row = ([None] * start) + row + ([None] * remaining_end)
    dense_map.append(row)

# Build faces
face_index = 0
row = 0
faces: List[List[Location]] = [None] * len(FACES_ROWWISE)
while face_index < len(FACES_ROWWISE):
    col = bounds_col[row][0]
    while col < bounds_col[row][1]:
        face = []
        for r in range(row, row + DIMENSION):
            for c in range(col, col + DIMENSION):
                location = dense_map[r][c]
                location.face = FACES_ROWWISE[face_index]
                location.face_point = (r - row, c - col)
                face.append(location)
        faces[FACES_ROWWISE[face_index]] = face
        face_index += 1
        col += DIMENSION
    row += DIMENSION

# Connect within faces
dirs = (RIGHT, DOWN, LEFT, UP)
for face in faces:
    assert len(face) == DIMENSION * DIMENSION
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            location = face[row * DIMENSION + col]
            for (vr, vc) in dirs:
                next_row = row + (-1 * vr)
                next_col = col + vc
                if 0 <= next_row < DIMENSION and 0 <= next_col < DIMENSION:
                    target = face[next_row * DIMENSION + next_col]
                    assert target is not location
                    location.connections[(vr, vc)] = target

face_dir_change = {}

# Connect across faces
# Example input
# connect(0, "b", 4, "t")
# connect(0, "r", 1, "t", reverse=True)
# connect(0, "t", 5, "b")
# connect(0, "l", 3, "r")
# connect(4, "r", 1, "l")
# connect(4, "b", 2, "b", reverse=True)
# connect(4, "l", 3, "b", reverse=True)
# connect(1, "b", 2, "l", reverse=True)
# connect(1, "r", 5, "r", reverse=True)
# connect(5, "t", 2, "t", reverse=True)
# connect(5, "l", 3, "t")
# connect(2, "r", 3, "l")

"""
  5511
  5511
  00
  00
3344
3344
22
22
"""

# Real input
connect(0, "b", 4, "t")
connect(0, "r", 1, "b")
connect(0, "t", 5, "b")
connect(0, "l", 3, "t")
connect(4, "r", 1, "r", reverse=True)
connect(4, "b", 2, "r")
connect(4, "l", 3, "r")
connect(1, "t", 2, "b")
connect(1, "l", 5, "r")
connect(5, "t", 2, "l")
connect(5, "l", 3, "l", reverse=True)
connect(2, "t", 3, "b")

assert len(face_dir_change) == 24

# Sanity check
for face in faces:
    for loc in face:
        assert len(loc.connections) == 4


def draw_map():
    for row in dense_map:
        for location in row:
            if location is None:
                print(" ", end="")
            elif location.point in steps:
                print(steps[location.point], end="")
            else:
                print(location.value, end="")
        print()
    input()


# Calculate movement
player = Player(point=map[0][0], dir=RIGHT)
steps = {}
for movement in movements:
    perform_movement(movement, player)
    # print(player.point.face, player.point.face_point, player.dir)
print((player.point.point[0] + 1) * 1000 + (player.point.point[1] + 1) * 4 + get_facing(player))

# 12585 too low
# 107021 too high
