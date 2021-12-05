import dataclasses
from typing import Tuple

import numpy as np


@dataclasses.dataclass
class Line:
    start: Tuple[int, int]
    end: Tuple[int, int]

    def is_axis_aligned(self) -> bool:
        return self.start[0] == self.end[0] or self.start[1] == self.end[1]

    def as_array(self) -> np.ndarray:
        return np.array([
            [*self.start],
            [*self.end]
        ])

    def mark(self, map: np.ndarray):
        pos = self.start
        dx = self.end[0] - self.start[0]
        if dx:
            dx = 1 if dx > 0 else -1
        dy = self.end[1] - self.start[1]
        if dy:
            dy = 1 if dy > 0 else -1

        while pos != self.end:
            map[pos[0], pos[1]] += 1
            pos = (pos[0] + dx, pos[1] + dy)
        map[pos[0], pos[1]] += 1


lines = []
with open("input.txt") as f:
    for line in f:
        start, end = line.split(" -> ")
        start = start.split(",")
        end = end.split(",")
        line = Line(
            start=(int(start[0]), int(start[1])),
            end=(int(end[0]), int(end[1])),
        )
        lines.append(line)

# lines = [l for l in lines if l.is_axis_aligned()]

lines_np = np.array([l.as_array() for l in lines])
max_x = lines_np[:, 0, :].max()
max_y = lines_np[:, 0, :].max()
print(max_x, max_y)

# x down, y right
map = np.zeros((max_x + 1, max_y + 1))
for line in lines:
    line.mark(map)
    print(line)
    print(map)
print(map[map >= 2].size)
