import collections
import dataclasses
from typing import FrozenSet, Optional, Tuple


@dataclasses.dataclass
class Valve:
    name: str
    flow_rate: int
    targets: Tuple[str]


valves = {}
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        line = line[6:]
        name = line[:line.index(" ")]
        line = line[len(name) + len(" has flow rate="):]
        flow_rate = int(line[:line.index(";")])
        line = line.split("to valve")[1]
        if line.startswith("s"):
            line = line[1:]
        targets = tuple(line.strip().split(", "))
        valves[name] = Valve(name=name, flow_rate=flow_rate, targets=targets)

max_steps = 26
valves_by_flow = sorted(list(valves.values()), key=lambda v: v.flow_rate, reverse=True)
valves_by_flow = [v for v in valves_by_flow if v.flow_rate > 0]

cache = {}
max_pressure = None


def calculate_total_pressure(step: int, valve: str) -> int:
    valve = valves[valve]
    remaining = max_steps - (step + 1)
    return valve.flow_rate * remaining


def potential_pressure(step: int, visited: FrozenSet[str]) -> int:
    remaining = collections.deque(v for v in valves_by_flow if v.name not in visited)
    total = 0
    for s in range(step, max_steps, 2):
        if len(remaining) == 0:
            break
        item = remaining.popleft()
        total += calculate_total_pressure(s, item.name)
        if len(remaining) > 0:
            item = remaining.popleft()
            total += calculate_total_pressure(s, item.name)
    return total


def has_remaining_valves(visited: FrozenSet[str]) -> bool:
    return any(v.name not in visited for v in valves_by_flow)


# @functools.lru_cache(1024 * 1024)
def calculate(step: int, valve: str, pressure: int, source: Optional[str], visited: FrozenSet[str]):
    global max_pressure

    key = (step, valve, pressure, visited)
    if key in cache:
        return cache[key]

    if max_pressure is not None and potential_pressure(step, visited) + pressure < max_pressure:
        cache[key] = pressure
        return pressure

    if step == max_steps or not has_remaining_valves(visited):
        if max_pressure is None or pressure > max_pressure:
            max_pressure = pressure
            print(pressure)
        cache[key] = pressure
        return pressure

    values = []
    if valves[valve].flow_rate > 0 and valve not in visited:
        values.append(
            calculate(step + 1, valve, pressure + calculate_total_pressure(step, valve), valve,
                      frozenset(visited | {valve})))

    for target in valves[valve].targets:
        if target != source:
            values.append(calculate(step + 1, target, pressure, valve, visited))

    return max(values, default=pressure)


def calculate_elephant(step: int, positions: Tuple[str, str], pressure: int, prev: Tuple[str, str],
                       visited: FrozenSet[str]):
    global max_pressure

    key = (step, tuple(sorted(positions)), pressure, visited)
    if key in cache:
        return cache[key]

    if max_pressure is not None and potential_pressure(step, visited) + pressure < max_pressure:
        cache[key] = pressure
        return pressure

    if step == max_steps or not has_remaining_valves(visited):
        if max_pressure is None or pressure > max_pressure:
            max_pressure = pressure
            print(pressure)
        cache[key] = pressure
        return pressure

    pos = positions[0]
    elephant = positions[1]

    # Open + elephant open
    if valves[pos].flow_rate > 0 and pos not in visited and valves[
        elephant].flow_rate > 0 and elephant not in visited and elephant != pos:
        calculate_elephant(step + 1, positions,
                           pressure + calculate_total_pressure(step, pos) + calculate_total_pressure(step, elephant),
                           positions, frozenset(visited | {pos, elephant}))

    # Open + elephant move
    if valves[pos].flow_rate > 0 and pos not in visited:
        for target2 in valves[elephant].targets:
            if target2 != prev[1]:
                calculate_elephant(step + 1, (positions[0], target2),
                                   pressure + calculate_total_pressure(step, pos),
                                   positions, frozenset(visited | {pos}))

    # Move + elephant open
    if valves[elephant].flow_rate > 0 and elephant not in visited:
        for target in valves[pos].targets:
            if target != prev[0]:
                calculate_elephant(step + 1, (target, positions[1]),
                                   pressure + calculate_total_pressure(step, elephant),
                                   positions, frozenset(visited | {elephant}))

    # Move + elephant move
    for target in valves[pos].targets:
        for target2 in valves[elephant].targets:
            if target != prev[0] and target2 != prev[1]:
                calculate_elephant(step + 1, (target, target2), pressure, positions, visited)


calculate_elephant(0, ("AA", "AA"), 0, [None, None], frozenset())
print(max_pressure)

# 2300 too low
