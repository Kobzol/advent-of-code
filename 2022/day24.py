import collections
import dataclasses
from typing import Optional, Set, Tuple

Point = Tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Blizzard:
    point: Point
    direction: str

    def __post_init__(self):
        assert self.direction in "<>^v"


@dataclasses.dataclass
class Result:
    time: Optional[int] = None


blizzards = set()
height = 0
with open("input.txt") as f:
    width = len(f.readline().strip()) - 2
    for (row, line) in enumerate(f):
        line = line.strip()[1:-1]
        if line.startswith("###"):
            break
        for (col, value) in enumerate(line):
            if value != ".":
                blizzards.add(Blizzard(point=(row, col), direction=value))
        height += 1

SOURCE = (-1, 0)
TARGET = (height, width - 1)


def calculate_distance(a: Point, b: Point) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def final_time_lb_staged(point: Point, timestep: int, stage: int) -> int:
    dist = 0
    if stage == 0:
        dist += calculate_distance(point, TARGET)
        dist += calculate_distance(SOURCE, TARGET) * 2
    elif stage == 1:
        dist += calculate_distance(point, SOURCE)
        dist += calculate_distance(SOURCE, TARGET)
    else:
        dist += calculate_distance(point, TARGET)

    return dist + timestep


def final_time_lb(point: Point, target: Point, timestep: int) -> int:
    return calculate_distance(point, target) + timestep


def build_timestep_map(timestep: int) -> Set[Point]:
    map = set()
    for blizzard in blizzards:
        (row, col) = blizzard.point
        if blizzard.direction == "v":
            row = (row + (timestep % height)) % height
        elif blizzard.direction == ">":
            col = (col + (timestep % width)) % width
        elif blizzard.direction == "^":
            row = ((row - (timestep % height)) + height) % height
        elif blizzard.direction == "<":
            col = ((col - (timestep % width)) + width) % width
        else:
            assert False
        map.add((row, col))
    return map


def is_clear(point: Point, map: Set[Point]) -> bool:
    if point not in (SOURCE, TARGET):
        if not (0 <= point[0] < height):
            return False
        if not (0 <= point[1] < width):
            return False

    return point not in map


def simulate_step_stage(point: Point, result: Result) -> True:
    states = collections.deque()
    states.append((point, 0, 0))

    cache = set()
    timestep_maps = {}

    step = 0
    while len(states):
        (point, timestep, stage) = states.pop()
        key = (point, timestep, stage)
        if key in cache:
            continue

        if point == TARGET and stage == 0:
            stage += 1
        elif point == SOURCE and stage == 1:
            stage += 1
        elif point == TARGET and stage == 2:
            if result.time is None or timestep < result.time:
                result.time = timestep
                print(timestep)
            cache.add(key)
            continue
        if result.time is not None and final_time_lb_staged(point, timestep, stage) >= result.time:
            cache.add(key)
            continue

        if (timestep + 1) not in timestep_maps:
            timestep_maps[(timestep + 1)] = build_timestep_map((timestep + 1))

        map = timestep_maps[timestep + 1]
        # map = build_timestep_map(timestep + 1)

        local_states = []
        down = (point[0] + 1, point[1])
        right = (point[0], point[1] + 1)
        up = (point[0] - 1, point[1])
        left = (point[0], point[1] - 1)

        if is_clear(up, map):
            local_states.append((up, timestep + 1, stage))
        if is_clear(left, map):
            local_states.append((left, timestep + 1, stage))
        if is_clear(right, map):
            local_states.append((right, timestep + 1, stage))
        if is_clear(down, map):
            local_states.append((down, timestep + 1, stage))
        if stage == 1:
            local_states.reverse()

        if not local_states:
            if is_clear(point, map) and (point, timestep + 1, stage) not in cache:
                states.append((point, timestep + 1, stage))
        else:
            states.extend(local_states)

        cache.add(key)
        step += 1
        if step % 1000 == 0:
            print(f"Step {step}, cache size {len(cache)}, point: {point}, stage: {stage}")


def simulate_step(point: Point, target: Point, timestep: int, result: Result, stage: int) -> True:
    states = collections.deque()
    states.append((point, timestep))

    cache = set()
    timestep_maps = {}

    step = 0
    while len(states):
        (point, timestep) = states.pop()
        timestep_norm = timestep % (width * height)
        if stage == 2:
            timestep_norm = timestep

        key = (point, timestep_norm)
        if key in cache:
            continue

        if point == target:
            if result.time is None or timestep <= result.time:
                result.time = timestep
                print(timestep)
            cache.add(key)
            continue

        if result.time is not None and final_time_lb(point, target, timestep) >= result.time:
            cache.add(key)
            continue

        if (timestep + 1) not in timestep_maps:
            timestep_maps[(timestep + 1)] = build_timestep_map((timestep + 1))

        map = timestep_maps[timestep + 1]
        # map = build_timestep_map(timestep + 1)

        local_states = []
        down = (point[0] + 1, point[1])
        right = (point[0], point[1] + 1)
        up = (point[0] - 1, point[1])
        left = (point[0], point[1] - 1)

        if stage != 1:
            if is_clear(left, map):
                local_states.append((left, timestep + 1))
            if is_clear(up, map):
                local_states.append((up, timestep + 1))
            if is_clear(right, map):
                local_states.append((right, timestep + 1))
            if is_clear(down, map):
                local_states.append((down, timestep + 1))
        else:
            if is_clear(down, map):
                local_states.append((down, timestep + 1))
            if is_clear(right, map):
                local_states.append((right, timestep + 1))
            if is_clear(left, map):
                local_states.append((left, timestep + 1))
            if is_clear(up, map):
                local_states.append((up, timestep + 1))
        if is_clear(point, map):  # and (point, (timestep + 1) % (width * height)) not in cache:
            states.append((point, timestep + 1))
        states.extend(local_states)

        cache.add(key)
        step += 1
        if step % 1000 == 0:
            print(f"Step {step}, cache size {len(cache)}, point: {point}")


# print(width, height)
# print(TARGET)
# result = Result()
# simulate_step(SOURCE, 0, result)
# print(result.time)

result_a = Result()
simulate_step(SOURCE, TARGET, 0, result=result_a, stage=0)
print(f"Stage 0: {result_a.time}")
time_a = result_a.time

result_b = Result()
simulate_step(TARGET, SOURCE, time_a, result=result_b, stage=1)
time_b = result_b.time - result_a.time
print(f"Stage 1: {time_b}")

result_c = Result()
simulate_step(SOURCE, TARGET, time_a + time_b, result=result_c, stage=2)
time_c = result_c.time - result_b.time
print(f"Stage 2: {time_c}")

print(time_a + time_b + time_c)
# print(result_a.time + result_b.time)
# print(result_a.time)

# 995 too high
# 700 too low
