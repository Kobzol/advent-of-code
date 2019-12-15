import traceback
from collections import deque

import numpy as np


class Program:
    def __init__(self, memory, input):
        self.memory = {}
        for i, item in enumerate(memory):
            self.memory[i] = item
        self.input = list(input[::-1])
        self.output = None
        self.pc = 0
        self.relbase = 0

    def add_input(self, c):
        self.input = [c] + self.input

    def read(self):
        return self.input.pop()

    def write(self, c):
        self.output = c

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


map = {}
directions = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}


def move(memory, direction):
    program = Program(memory, (direction, ))
    while True:
        program.output = None
        end = run_inst(program)
        assert not end
        if program.output is not None:
            new_mem = [0] * (max(program.memory) + 1)
            for (index, value) in program.memory.items():
                new_mem[index] = value
            return (program.output, new_mem)


def find():
    queue = deque()
    queue.append(((0, 0), list(memory), 0))

    while len(queue) > 0:
        position, mem_state, distance = queue.pop()
        if position in map:
            continue

        map[position] = {
            "state": "visited",
            "distance": distance
        }
        for (dir_index, (x, y)) in directions.items():
            target_pos = (position[0] + x, position[1] + y)
            if target_pos in map:
                continue
            ret, new_mem = move(mem_state, dir_index)
            if ret == 0:
                map[target_pos] = {
                    "state": "wall"
                }
            elif ret == 1:
                queue.append((target_pos, new_mem, distance + 1))
            elif ret == 2:
                return (target_pos, new_mem, distance + 1)


target_pos, new_mem, distance = find()
print(target_pos, distance)
map.clear()


def fill_oxygen(start_pos, memory):
    max_dist = 0

    queue = deque()
    queue.append((start_pos, list(memory), 0))

    while len(queue) > 0:
        position, mem_state, distance = queue.popleft()
        if position in map:
            continue
        max_dist = max(max_dist, distance)

        map[position] = {
            "state": "visited",
            "distance": distance
        }
        for (dir_index, (x, y)) in directions.items():
            target_pos = (position[0] + x, position[1] + y)
            if target_pos in map:
                continue
            ret, new_mem = move(mem_state, dir_index)
            if ret == 0:
                map[target_pos] = {
                    "state": "wall"
                }
            elif ret in (1, 2):
                queue.append((target_pos, new_mem, distance + 1))
    return max_dist


max_dist = fill_oxygen(target_pos, new_mem)
print(max_dist)


def draw(f):
    min_x = min(pos[0] for pos in map)
    max_x = max(pos[0] for pos in map)
    min_y = min(pos[1] for pos in map)
    max_y = max(pos[1] for pos in map)

    offset_x = 0 - min_x
    offset_y = 0 - min_y

    out_map = np.zeros((max_x - min_x + 1, max_y - min_y + 1))

    for ((x, y), state) in map.items():
        if state["state"] == "wall":
            out_map[x + offset_x, y + offset_y] = 1
        elif state["state"] == "visited":
            out_map[x + offset_x, y + offset_y] = 2

    for row in range(out_map.shape[1]):
        for col in range(out_map.shape[0]):
            val = ' '
            if out_map[col, row] == 1:
                val = '#'
            elif out_map[col, row] == 2:
                val = '.'
            print(val, end='', file=f)
        print(file=f)


# with open("out.txt", "w") as f:
#     draw(f)

# 402 too high
