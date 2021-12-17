import dataclasses
import math


@dataclasses.dataclass
class Point:
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Probe:
    velocity: Point
    position: Point = Point(x=0, y=0)

    def move(self) -> "Probe":
        pos = dataclasses.replace(self.position)
        pos.x += self.velocity.x
        pos.y += self.velocity.y
        vel = dataclasses.replace(self.velocity)
        if vel.x:
            vel.x = int(vel.x - math.copysign(1, vel.x))
        vel.y -= 1
        return Probe(position=pos, velocity=vel)


with open("input.txt") as f:
    line = f.readline().strip()
    line = line[line.index(":") + 2:]
    x, y = line.split(", ")
    x = x[2:].split("..")
    target_x = int(x[0]), int(x[1])
    y = y[2:].split("..")
    target_y = int(y[0]), int(y[1])


def is_inside_target(probe: Probe) -> bool:
    return target_x[0] <= probe.position.x <= target_x[1] and target_y[0] <= probe.position.y <= \
           target_y[1]


@dataclasses.dataclass
class Result:
    max_y: int
    offset: int = 0
    hit: bool = False


def reaches_target(probe: Probe) -> Result:
    max_y = probe.position.y

    while True:
        # print(probe)
        if is_inside_target(probe):
            return Result(max_y=max_y, hit=True)
        elif probe.position.x > target_x[1]:
            return Result(max_y=max_y, offset=1)
        elif probe.position.y < target_y[0]:
            return Result(max_y=max_y, offset=-1)
        probe = probe.move()
        max_y = max(max_y, probe.position.y)


max_y = 0
initial_y = 1000
initial_x = 1
results = set()

while initial_y >= target_y[0] and initial_x <= target_x[1]:
    probe = Probe(velocity=Point(x=initial_x, y=initial_y))
    result = reaches_target(probe)
    if result.hit:
        results.add((initial_x, initial_y))
    # if result.offset == -1:
    #     initial_x += 1
    # elif result.offset == 1:
    #     initial_y -= 1
    #     initial_x = 0
    # print(initial_x, initial_y)
    initial_x += 1
    if initial_x > target_x[1]:
        initial_x = 1
        initial_y -= 1
    # print(initial_x, initial_y)

# 3570 too low
print(len(results))
