import dataclasses
import itertools
from collections import Counter
from typing import List, Optional, Tuple

import tqdm

Range = Tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Cube:
    x: Range = (0, 0)
    y: Range = (0, 0)
    z: Range = (0, 0)

    def __post_init__(self):
        assert self.x[1] >= self.x[0]
        assert self.y[1] >= self.y[0]
        assert self.z[1] >= self.z[0]

    def __lt__(self, other: "Cube"):
        return self.axes() < other.axes()

    def axes(self):
        return (self.x, self.y, self.z)

    def point_count(self) -> int:
        x = (self.x[1] - self.x[0]) + 1
        y = (self.y[1] - self.y[0]) + 1
        z = (self.z[1] - self.z[0]) + 1
        return x * y * z

    def corner_points(self):
        points = set()
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    points.add((self.x[i], self.y[j], self.z[k]))
        return points

    def is_thin(self) -> bool:
        return any(v[0] == v[1] for v in self.axes())

    def intersection(self, cube: "Cube") -> Optional["Cube"]:
        x = intersect_axis(self.x, cube.x)
        y = intersect_axis(self.y, cube.y)
        z = intersect_axis(self.z, cube.z)

        if x is None or y is None or z is None:
            return None

        return Cube(x=x, y=y, z=z)

    def cut(self, axis_index: int, axis: Range) -> List["Cube"]:
        axes = list(self.axes())
        my_axis = axes[axis_index]
        cubes = []

        if my_axis == axis or intersect_axis(my_axis, axis) is None:
            cubes.append(self)
        elif my_axis[0] == axis[0]:
            axes[axis_index] = (my_axis[0], axis[1])
            cubes.append(Cube(*axes))
            axes[axis_index] = (axis[1] + 1, my_axis[1])
            cubes.append(Cube(*axes))
        elif my_axis[1] == axis[1]:
            axes[axis_index] = (my_axis[0], axis[0] - 1)
            cubes.append(Cube(*axes))
            axes[axis_index] = (axis[0], my_axis[1])
            cubes.append(Cube(*axes))
        else:
            axes[axis_index] = (my_axis[0], axis[0] - 1)
            cubes.append(Cube(*axes))
            axes[axis_index] = (axis[0], axis[1])
            cubes.append(Cube(*axes))
            axes[axis_index] = (axis[1] + 1, my_axis[1])
            cubes.append(Cube(*axes))
        return cubes

    def split_to_disjoint(self, cube: "Cube") -> List["Cube"]:
        """
        Splits `self` into pieces disjoint with `cube`.
        """
        overlap = self.intersection(cube)
        if overlap is None:
            return [self]
        assert not overlap.contains(self)
        # Cut by X
        cubes = self.cut(0, overlap.x)
        # Cut by Y
        cubes = list(itertools.chain.from_iterable([c.cut(1, overlap.y) for c in cubes]))
        # Cut by Z
        cubes = list(itertools.chain.from_iterable([c.cut(2, overlap.z) for c in cubes]))

        cubes = [c for c in cubes if not overlap.contains(c)]

        return cubes

    def contains(self, cube: "Cube") -> bool:
        return (
                self.x[0] <= cube.x[0] <= cube.x[1] <= self.x[1] and
                self.y[0] <= cube.y[0] <= cube.y[1] <= self.y[1] and
                self.z[0] <= cube.z[0] <= cube.z[1] <= self.z[1]
        )

    def reduce(self, cube: "Cube") -> List["Cube"]:
        overlap = self.intersection(cube)
        if overlap is None:
            return [self]
        assert not overlap.contains(self)

        # Cut by X
        cubes = self.cut(0, overlap.x)
        # Cut by Y
        cubes = list(itertools.chain.from_iterable([c.cut(1, overlap.y) for c in cubes]))
        # Cut by Z
        cubes = list(itertools.chain.from_iterable([c.cut(2, overlap.z) for c in cubes]))

        cubes = [c for c in cubes if not overlap.contains(c)]

        return cubes


def intersect_axis(a1: Range, a2: Range) -> Optional[Range]:
    if a1[1] < a2[0]:
        return None
    if a1[0] > a2[1]:
        return None

    start = max(a1[0], a2[0])
    end = min(a1[1], a2[1])
    return (start, end)


@dataclasses.dataclass(frozen=True)
class Command:
    on: bool
    cube: Cube

    def range(self, bounds):
        start = max(bounds[0], -50)
        end = min(bounds[1], 50)
        return range(start, end + 1)

    def iterate_points(self):
        for x in self.range(self.cube.x):
            for y in self.range(self.cube.y):
                for z in self.range(self.cube.z):
                    yield (x, y, z)


commands = []
with open("input.txt") as f:
    for line in f:
        if line[0] == "#":
            continue
        cmd, bounds = line.strip().split(" ")
        on = cmd.strip() == "on"
        x, y, z = bounds.split(",")
        x = tuple(int(v) for v in x[2:].split(".."))
        y = tuple(int(v) for v in y[2:].split(".."))
        z = tuple(int(v) for v in z[2:].split(".."))
        commands.append(Command(on=on, cube=Cube(x=x, y=y, z=z)))

cubes = set()
for command in tqdm.tqdm(commands):
    cubes = {c for c in cubes if not command.cube.contains(c)}
    if command.on:
        if not cubes:
            cubes.add(command.cube)
            continue
        new_cubes = set()
        for cube in list(cubes):
            for splitted in cube.split_to_disjoint(command.cube):
                # if not any(c.contains(splitted) for c in new_cubes):
                new_cubes.add(splitted)
        new_cubes.add(command.cube)
        cubes = new_cubes
    else:
        new_cubes = set()
        for cube in cubes:
            for reduced in cube.reduce(command.cube):
                new_cubes.add(reduced)
        cubes = new_cubes
    # new_cubes = set()
    # for cube in cubes:
    #     if any(c != cube and c.contains(cube) for c in cubes):
    #         continue
    #     new_cubes.add(cube)
    # cubes = new_cubes

    # for (a, b) in itertools.product(cubes, cubes):
    #     if a != b:
    #         assert not a.contains(b)
    #         assert not b.contains(a)

for cube in sorted(cubes):
    print(cube)

point_count = sum(c.point_count() for c in cubes)
print(point_count)

corner_points = Counter()
for cube in cubes:
    for point in cube.corner_points():
        corner_points[point] += 1
corner_points = {k: v - 1 for (k, v) in corner_points.items()}

point_count -= sum(corner_points.values())
print(point_count)
print(point_count - 2758514936282235)

# 2759022355480338
# 2759022355474021
# 2758796594581508

# 2758514936282235
