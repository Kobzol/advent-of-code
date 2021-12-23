import dataclasses
import functools
import math
from typing import Dict, Tuple

Point = Tuple[int, int]

HALLWAY_Y = 4


@dataclasses.dataclass(frozen=True)
class State:
    positions: Tuple[Point, str]

    def target_positions(self, amphibod: str):
        x = amphibod_index(amphibod) * 2
        for i in range(4):
            yield (x, i)

    def expand(self):
        pos_map = dict(self.positions)

        for (pos, amphibod) in self.positions:
            target_positions = tuple(self.target_positions(amphibod))
            if is_in_sideroom(pos):
                sideroom_positions = tuple(self.target_positions("ABCD"[pos[0] // 2]))
                sideroom_idx = sideroom_positions.index(pos)
                if pos in target_positions:
                    # We are at the final position
                    if all(pos_map.get(p) == amphibod for p in sideroom_positions[:sideroom_idx]):
                        continue
                # We cannot move
                if any(p in pos_map for p in sideroom_positions[sideroom_idx + 1:]):
                    continue

                # Moving out of sideroom
                for (new_pos, cost) in self.generate_positions_side_room(pos, pos_map, amphibod):
                    yield (self.move(pos_map, pos, new_pos, amphibod), cost)
            elif is_in_hallway(pos):
                to_target = self.gen_positions_hallway_to_room(pos, pos_map, amphibod)
                if to_target:
                    cost = amphibod_cost(amphibod) * len(to_target)
                    new_pos = to_target[-1]
                    yield (self.move(pos_map, pos, new_pos, amphibod), cost)
            else:
                assert False

    def move(self, pos_map: Dict[Point, str], orig_pos: Point, new_pos: Point,
             amphibod: str) -> "State":
        pos_map = dict(pos_map)
        assert pos_map[orig_pos] == amphibod
        del pos_map[orig_pos]
        assert new_pos not in pos_map
        pos_map[new_pos] = amphibod
        positions = pos_map.items()
        return create_state(positions=positions)

    def gen_positions_hallway_to_room(self, pos: Point, pos_map: Dict[Point, str], amphibod: str):
        target_positions = tuple(reversed(tuple(self.target_positions(amphibod))))
        if any(pos_map.get(p, amphibod) != amphibod for p in target_positions):
            return

        x = target_positions[0][0]
        assert pos[0] != x
        to_right = x > pos[0]
        positions = []

        while pos[0] != x:
            if to_right:
                pos = right(pos)
            else:
                pos = left(pos)
            if pos in pos_map:
                return
            positions.append(pos)

        for pos in target_positions:
            if pos not in pos_map:
                positions.append(pos)
            else:
                break
        return positions

    def generate_positions_side_room(self, pos: Point, pos_map: Dict[Point, str], amphibod: str):
        cost = amphibod_cost(amphibod)
        total_cost = 0

        # Move to hallway
        while pos[1] != HALLWAY_Y:
            pos = up(pos)
            assert pos not in pos_map
            total_cost += cost

        # Move right to target
        to_target = self.gen_positions_hallway_to_room(pos, pos_map, amphibod)
        if to_target:
            total_cost += cost * len(to_target)
            yield (to_target[-1], total_cost)

        state = (pos, total_cost)

        # Now we are in the blocking spot, we have to move
        # Move left
        while True:
            l = left(pos)
            if is_valid_pos(l) and l not in pos_map:
                pos = l
                total_cost += cost
                if not is_hallway_blocking(l):
                    yield (pos, total_cost)
            else:
                break

        pos, total_cost = state
        # Move right
        while True:
            r = right(pos)
            if is_valid_pos(r) and r not in pos_map:
                pos = r
                total_cost += cost
                if not is_hallway_blocking(r):
                    yield (pos, total_cost)
            else:
                break

    def __repr__(self):
        ret = """#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  #########"""
        ret = list(list(row) for row in ret.split("\n"))
        for (pos, amphibod) in self.positions:
            row = pos[1]
            col = pos[0]
            row = (4 - row) + 1
            col = col + 3
            ret[row][col] = amphibod
        return "\n".join("".join(row) for row in ret)


def create_state(positions: Tuple[Point, str]) -> State:
    return State(positions=tuple(sorted(positions)))


def up(pos: Point) -> Point:
    return (pos[0], pos[1] + 1)


def down(pos: Point) -> Point:
    return (pos[0], pos[1] - 1)


def left(pos: Point) -> Point:
    return (pos[0] - 1, pos[1])


def right(pos: Point) -> Point:
    return (pos[0] + 1, pos[1])


def amphibod_cost(amphibod: str) -> int:
    return int(math.pow(10, amphibod_index(amphibod)))


def amphibod_index(amphibod: str) -> int:
    return "ABCD".index(amphibod)


def is_in_hallway(point: Point) -> bool:
    return -2 <= point[0] <= 8 and point[1] == HALLWAY_Y


def is_in_sideroom(point: Point) -> bool:
    return point[0] in (0, 2, 4, 6) and point[1] in (0, 1, 2, 3)


def is_hallway_blocking(point: Point) -> bool:
    return is_in_hallway(point) and point[0] in (0, 2, 4, 6)


def is_valid_pos(point: Point) -> bool:
    return is_in_sideroom(point) or is_in_hallway(point)


# x right, y up

start = create_state([
    ((0, 0), "D"),
    ((0, 1), "D"),
    ((0, 2), "D"),
    ((0, 3), "B"),
    ((2, 0), "C"),
    ((2, 1), "B"),
    ((2, 2), "C"),
    ((2, 3), "B"),
    ((4, 0), "A"),
    ((4, 1), "A"),
    ((4, 2), "B"),
    ((4, 3), "C"),
    ((6, 0), "A"),
    ((6, 1), "C"),
    ((6, 2), "A"),
    ((6, 3), "D"),
])
end = create_state([
    ((0, 0), "A"),
    ((0, 1), "A"),
    ((0, 2), "A"),
    ((0, 3), "A"),
    ((2, 0), "B"),
    ((2, 1), "B"),
    ((2, 2), "B"),
    ((2, 3), "B"),
    ((4, 0), "C"),
    ((4, 1), "C"),
    ((4, 2), "C"),
    ((4, 3), "C"),
    ((6, 0), "D"),
    ((6, 1), "D"),
    ((6, 2), "D"),
    ((6, 3), "D"),
])
# print(start)
# for (next_state, _) in start.expand():
#     print(next_state)
#     print()
# exit()


# visited = set()
# distances = {}
# distances[start] = 0
# stack = [(start, 0)]
# while stack:
#     stack = sorted(stack, key=lambda v: v[1])
#     state, cost = stack.pop()
#     if state in visited:
#         continue
#
#     for (next_state, next_cost) in state.expand():
#         c = cost + next_cost
#         if next_state not in distances or distances[next_state] > c:
#             distances[next_state] = c
#         stack.append((next_state, c))
#     visited.add(state)
#
# print(distances[end])

visited = {}
min_dist = {}


@functools.lru_cache(maxsize=None)
def solve(state: State) -> int:
    if state == end:
        return 0
    distance = 10e6
    for (next_state, next_cost) in state.expand():
        from_next = solve(next_state)
        distance = min(distance, from_next + next_cost)
    return distance


result = solve(start)
print(result)

# 15111

# graph = nx.DiGraph()
# stack = [(start, 0)]
# visited = {start}
# while stack:
#     state, current_cost = stack.pop()
#     assert state in visited
#     for (next_state, cost) in state.expand():
#         graph.add_edge(state, next_state, weight=current_cost + cost)
#         if next_state not in visited:
#             visited.add(next_state)
#             stack.append((next_state, current_cost + cost))
#
# print("Graph built")
#
# path = nx.shortest_path(graph, start, end, weight="weight")
# cost = 0
# for i in range(len(path) - 1):
#     cost += graph[path[i]][path[i + 1]]["weight"]
#     print(path[i])
# print(len(path))
# print(cost)
