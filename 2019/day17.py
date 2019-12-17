import os
import traceback
import numpy as np


class Program:
    def __init__(self, memory, input):
        self.memory = {}
        for i, item in enumerate(memory):
            self.memory[i] = item
        self.input = list(input[::-1])
        self.output = []
        self.pc = 0
        self.relbase = 0

    def add_input(self, c):
        self.input = [c] + self.input

    def read(self):
        return self.input.pop()

    def write(self, c):
        self.output.append(c)

    def memread(self, address):
        if isinstance(address, Arg):
            address = address.address_eval()
        assert address >= 0
        if address not in self.memory:
            self.memory[address] = 0
        return self.memory[address]

    def memwrite(self, address, value):
        if isinstance(address, Arg):
            address = address.address_eval()
        self.memory[address] = value


class Arg:
    def __init__(self, val, mode, program):
        self.val = val
        self.mode = mode
        self.program = program

    def eval(self):
        if self.mode == 0:
            return self.program.memread(self.val)
        elif self.mode == 1:
            return self.val
        elif self.mode == 2:
            return self.program.memread(self.val + self.program.relbase)
        else:
            assert False

    def address_eval(self):
        assert self.mode != 1
        if self.mode == 2:
            return self.val + self.program.relbase
        return self.val


def stop(program, args):
    return True


def add(program, args):
    program.memwrite(args[2], args[0].eval() + args[1].eval())


def mul(program, args):
    program.memwrite(args[2], args[0].eval() * args[1].eval())


def read(program, args):
    program.memwrite(args[0], program.read())


def write(program, args):
    program.write(args[0].eval())


def jumpiftrue(program, args):
    if args[0].eval() != 0:
        return args[1].eval()


def jumpiffalse(program, args):
    if args[0].eval() == 0:
        return args[1].eval()


def lessthan(program, args):
    val = 0
    if args[0].eval() < args[1].eval():
        val = 1
    program.memwrite(args[2], val)


def equals(program, args):
    val = 0
    if args[0].eval() == args[1].eval():
        val = 1
    program.memwrite(args[2], val)


def modify_relbase(program, args):
    program.relbase += args[0].eval()


instructions = {
    99: (0, stop),
    1: (3, add),
    2: (3, mul),
    3: (1, read),
    4: (1, write),
    5: (2, jumpiftrue),
    6: (2, jumpiffalse),
    7: (3, lessthan),
    8: (3, equals),
    9: (1, modify_relbase)
}


def run_inst(program):
    try:
        opcode = program.memread(program.pc) % 100
        (param_count, fn) = instructions[opcode]
        modes = list(int(c) for c in str(program.memread(program.pc) // 100)[::-1])
        modes += [0] * (param_count - len(modes))
        args = tuple(Arg(v, m, program) for (v, m) in
                     zip((program.memread(a) for a in
                          range(program.pc + 1, program.pc + 1 + param_count)), modes))
        ret = fn(program, args)
        if ret is True:
            return True
        elif isinstance(ret, int):
            program.pc = ret
        else:
            program.pc += 1 + param_count
    except:
        traceback.print_exc()
    return False


with open("input.txt") as f:
    memory = list(int(v) for v in f.read().strip().split(","))

"""program = Program(memory, ())

while not run_inst(program):
    pass

map = [[]]
for i in program.output:
    ch = chr(i)
    if ch == "\n":
        map.append([])
    else:
        map[-1].append(ch)

map.pop()"""

map = """
..................#############........
..................#...........#........
..................#...........#........
..................#...........#........
..................#...........#........
..................#...........#........
..................#...........#........
..................#...........#........
..............#####...........#........
..............#...............#........
..............#...........#####........
..............#...........#............
......########O##.........#............
......#.......#.#.........#............
......#.......#.#.........#............
......#.......#.#.........#............
......#.....##O##.........#............
......#.....#.#...........#............
......#.....#.#########...#########....
......#.....#.........#...........#....
......#.....#.........#...........#....
......#.....#.........#...........#....
......#.....#.........#...........#....
......#.....#.........#...........#....
......######O##.....##O########...#....
............#.#.....#.#.......#...#....
............##O#####O##.....##O###O####
..............#.....#.......#.#...#...#
..............#.....#.......#.#####...#
..............#.....#.......#.........#
#####.........#.....#.......#.........#
#...#.........#.....#.......#..........
#...#.......##O#####O##.....#..........
#...#.......#.#.....#.#.....#..........
#...########O##.....##O######..........
#...........#.........#................
#...........#.........#................
#...........#.........#................
#...........#.........#................
#...........#.........#................
#############.........#................
......................#................
..................^####................
"""

map = [list(row) for row in map.strip().split("\n")]


def print_map(map, print_junctions=True):
    for ri, row in enumerate(map):
        for ci, col in enumerate(row):
            if print_junctions and is_junction(map, ri, ci):
                col = 'O'
            print(col, end="")
        print()


def is_valid(map, row, col):
    return row >= 0 and row < len(map) and 0 <= col < len(map[row])


def is_junction(map, row, col):
    offsets = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
        (0, 0)
    )
    return all(is_valid(map, row + x, col + y) and map[row + x][col + y] == '#' for (x, y) in offsets)


def sum_junctions(map):
    s = 0
    for ri, row in enumerate(map):
        for ci, col in enumerate(row):
            if is_junction(map, ri, ci):
                s += ri * ci
    return s


def find_robot(map):
    for ri, row in enumerate(map):
        for ci, col in enumerate(row):
            if col == '^':
                return (ri, ci)
    assert False


def turn_right(dir):
    return (dir[1], -dir[0])


def turn_left(dir):
    return (-dir[1], dir[0])


def turn(position, new_position, dir):
    if (position[0] + dir[0], position[1] + dir[1]) == new_position:
        return (dir, None)
    new_dir = (new_position[0] - position[0], new_position[1] - position[1])
    if new_dir == turn_right(dir):
        return (new_dir, ["R"])
    elif new_dir == turn_left(dir):
        return (new_dir, ["L"])
    else:
        return None  # (new_dir, ["R", "R"])


def find_paths(map, path, position, dir, visited, visited_pos):
    path = list(path)
    path.append(position)
    visited.add(position)
    visited_pos.add((position, dir))

    if len(visited) == full_count:
        paths.add(tuple(path))
        return

    offsets = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    )
    row, col = position
    for (x, y) in offsets:
        target_pos = (row + x, col + y)
        if is_valid(map, target_pos[0], target_pos[1]) and map[target_pos[0]][target_pos[1]] == '#':
            res = turn(position, target_pos, dir)
            if res is None:
                continue
            new_dir, turn_cmds = res
            if (target_pos, new_dir) in visited_pos:
                continue
            new_path = list(path)
            if turn_cmds is not None:
                new_path += turn_cmds
            find_paths(map, new_path, target_pos, new_dir, set(visited), set(visited_pos))


"""
paths = set()

print(full_count, robot_position)
print_map(map)

find_paths(map, (), robot_position, (-1, 0), set(), set())
print(paths)"""


def print_path(map, path):
    m = [list(r) for r in map]
    index = 0
    for i, p in enumerate(path):
        if isinstance(p, tuple):
            print(p, i, end=", ")
            m[p[0]][p[1]] = str(index % 9)
            index += 1
    print_map(m, False)


full_count = sum(sum(1 if c == '#' else 0 for c in r) for r in map) + 1
robot_position = find_robot(map)
functions = {
    "A": ("R", 4, "L", 10, "L", 10),
    "B": ("L", 8, "L", 8, "R", 10, "R", 4),
    "C": ("L", 8, "R", 12, "R", 10, "R", 4)
}
program = ["A", "C", "A", "C", "A", "B", "C", "B", "A", "B"]

path = ("R", 4, "L", 10, "L", 10, "L", 8, "R", 12, "R", 10, "R", 4, "R", 4, "L", 10, "L", 10, "L", 8, "R", 12, "R", 10, "R", 4,
            "R", 4, "L", 10, "L", 10, "L", 8, "L", 8, "R", 10, "R", 4, "L", 8, "R", 12, "R", 10, "R", 4, "L", 8, "L", 8,
          "R", 10, "R", 4, "R", 4, "L", 10, "L", 10, "L", 8, "L", 8, "R", 10, "R", 4)


def assign(fns, visited, remaining):
    if remaining == 0:
        assert all(visited)
        print(fns)
        print(visited)
        return
    elif len(fns) == 3:
        return

    for length in range(9, 2, -1):
        end = len(path) - length
        for i in range(0, end):
            current = path[i:i + length]
            if len(",".join(str(x) for x in current)) > 20:
                continue
            if any(visited[i:i+length]):
                continue

            candidates = []
            for j in range(i + length, end):
                target = path[j:j + length]
                if any(visited[j:j + length]):
                    continue
                if current == target:
                    candidates.append(j)

            f = fns + [(current, [i] + candidates)]
            v = list(visited)
            v[i:i+length] = [True] * length
            rem = remaining - length
            for cand in candidates:
                v[cand:cand+length] = [True] * length
                rem -= length
            assign(f, v, rem)

"""print(len(path))
assign([], [False for _ in path], len(path))
exit()"""


robot_dir = (-1, 0)
visited = set()

pc = 0
fc = 0


def visit(position):
    if not is_valid(map, position[0], position[1]) or map[position[0]][position[1]] == '.':
        raise Exception("")
    map[robot_position[0]][robot_position[1]] = 'X'
    return False


while pc < len(program):
    visited.add(robot_position)
    function = functions[program[pc]]
    command = functions[program[pc]][fc]
    if visit(robot_position):
        break

    if command == "R":
        robot_dir = turn_right(robot_dir)
    elif command == "L":
        robot_dir = turn_left(robot_dir)
    else:
        for _ in range(command):
            robot_position = (robot_position[0] + robot_dir[0], robot_position[1] + robot_dir[1])
            visited.add(robot_position)
            if visit(robot_position):
                break

    fc += 1
    if fc >= len(function):
        fc = 0
        pc += 1


print(len(visited), full_count)
print_map(map, False)

input_str = ",".join(program) + "\n"
for fn in ("A", "B", "C"):
    input_str += ",".join(str(x) for x in functions[fn]) + "\n"
input_str += "n\n"

memory[0] = 2
program = Program(memory, list(ord(c) for c in input_str))

while not run_inst(program):
    pass

print(max(program.output), program.output)

# 120 too low
