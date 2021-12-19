import dataclasses
from typing import Optional, Tuple


@dataclasses.dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0
    z: int = 0

    def __sub__(self, other) -> "Point":
        assert isinstance(other, Point)
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other) -> "Point":
        assert isinstance(other, Point)
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Point(x=-self.x, y=-self.y, z=-self.z)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.as_tuple() == other.as_tuple()

    def as_tuple(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return f"[{self.x},{self.y},{self.z}]"


@dataclasses.dataclass(frozen=True)
class N:
    index: int

    def resolve(self, data):
        return -data[self.index]


@dataclasses.dataclass(frozen=True)
class P:
    index: int

    def resolve(self, data):
        return data[self.index]


@dataclasses.dataclass(frozen=True)
class Scanner:
    points: Tuple[Point]
    index: int

    def offset(self, point: Point) -> "Scanner":
        return Scanner(points=tuple(p + point for p in self.points), index=self.index)

    def get_rotations(self):
        perms = (
            (P(0), P(1), P(2)),  # X
            (N(0), P(1), N(2)),  # -X
            (P(1), N(0), P(2)),  # Y
            (N(1), P(0), P(2)),  # -Y
            (P(2), P(1), N(0)),  # Z
            (N(2), P(1), P(0))  # -Z
        )
        perms2 = (
            (P(1), P(2)),
            (P(2), N(1)),
            (N(1), N(2)),
            (N(2), P(1))
        )

        def gen_point(point: Point, perm, perm2) -> Point:
            point = point.as_tuple()
            point = list(index.resolve(point) for index in perm)
            point[1:] = list(index.resolve(point) for index in perm2)
            return Point(*tuple(point))

        for perm in perms:
            for perm2 in perms2:
                yield Scanner(
                    points=tuple(gen_point(p, perm, perm2) for p in self.points), index=self.index)


scanners = []
points = []
index = 0
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if "," in line:
            nums = [int(v) for v in line.split(",")]
            points.append(Point(x=nums[0], y=nums[1], z=nums[2]))
        if not line:
            scanners.append(Scanner(points=tuple(points), index=index))
            index += 1
            points = []
assert points
scanners.append(Scanner(points=tuple(points), index=index))


def find_offset(a: Scanner, b: Scanner) -> Optional[Tuple[Point, Scanner]]:
    b_rotations = list(b.get_rotations())
    for point_a in a.points:
        for rotated_b in b_rotations:
            set_b = set(rotated_b.points)
            for point_b in rotated_b.points[:-11]:
                offset = point_b - point_a
                offset_a = a.offset(offset)
                set_a = set(offset_a.points)
                intersection = set_a.intersection(set_b)
                if len(intersection) >= 12:
                    assert point_b in intersection
                    return (-offset, rotated_b)
    return None


resolved = {scanners[0]: Point()}
remaining = scanners[1:]

while remaining:
    for (scanner, ref_offset) in reversed(resolved.items()):
        match = None
        for other in remaining:
            result = find_offset(scanner, other)
            if result is not None:
                (offset, moved_scanner) = result
                print(
                    f"Matched {scanner.index} with {other.index}: {offset}, {offset + ref_offset}")
                match = (other, moved_scanner, offset)
                break
        if match is not None:
            other, moved_scanner, offset = match
            remaining.remove(other)
            resolved[moved_scanner] = ref_offset + offset
            break

points = set()
for (scanner, offset) in resolved.items():
    moved_points = scanner.offset(offset).points
    moved_points = set((p.as_tuple() for p in moved_points))
    points = points.union(moved_points)
print(len(points))
