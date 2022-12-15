import dataclasses
import itertools
from typing import List, Tuple

from tqdm import tqdm

Point = Tuple[int, int]


@dataclasses.dataclass
class Sensor:
    point: Point
    beacon: Point


def distance(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@dataclasses.dataclass
class Range:
    start: int
    end: int

    def split(self, start: int, end: int) -> List["Range"]:
        # Outside
        if end < self.start or start > self.end:
            return [self]
        # Erases whole range
        if start <= self.start and end >= self.end:
            return []
        # Overlap
        ranges = []
        if self.start < start:
            ranges.append(Range(self.start, start - 1))
        if self.end > end:
            ranges.append(Range(end + 1, self.end))
        return ranges


sensors = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        a, b = line.split(": closest beacon is at ")
        a = a[len("Sensor at x="):]
        x1, x2 = a.split(", ")
        x = int(x1)
        y = int(x2[2:])
        x1, x2 = b.split(", ")
        bx = int(x1[2:])
        by = int(x2[2:])
        sensors.append(Sensor(
            point=(x, y),
            beacon=(bx, by)
        ))
max_dist = max(distance(s.point, s.beacon) for s in sensors) + 1
min_x = min(s.point[0] for s in sensors)
max_x = max(s.point[0] for s in sensors)
beacons = set(s.beacon for s in sensors)

print(min_x, max_x, max_dist)

row_count = 4000000

for row in tqdm(range(row_count)):
    ranges = [Range(0, row_count)]
    for sensor in sensors:
        dist = distance(sensor.point, sensor.beacon)
        x = sensor.point[0]
        # Too far vertically
        if distance(sensor.point, (x, row)) > dist:
            continue
        y_diff = abs(row - sensor.point[1])
        x_start = x - (dist - y_diff)
        x_end = x + (dist - y_diff)
        ranges = list(itertools.chain.from_iterable(r.split(x_start, x_end) for r in ranges))
        a = 5
    if len(ranges) > 0:
        assert len(ranges) == 1
        assert ranges[0].start == ranges[0].end
        x = ranges[0].start
        print(x * 4000000 + row)
        break
