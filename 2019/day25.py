import itertools
import traceback


class Program:
    def __init__(self, memory, input):
        self.memory = {}
        if isinstance(memory, dict):
            self.memory = dict(memory)
        else:
            for i, item in enumerate(memory):
                self.memory[i] = item
        self.input = list(input[::-1])
        self.output = []
        self.pc = 0
        self.relbase = 0

    def copy(self):
        assert len(self.input) == 0
        program = Program(self.memory, ())
        program.pc = self.pc
        program.relbase = self.relbase
        program.output = self.output
        return program

    def add_input(self, c):
        self.input = [c] + self.input

    def set_input_str(self, c):
        self.input = list(ord(x) for x in c[::-1])

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

    def output_as_str(self):
        return "".join(chr(c) for c in self.output)


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


def run_until_input(program):
    while True:
        ret = run_inst(program)
        if ret:
            return True
        if program.output_as_str().endswith("Command?"):
            return False


def execute_commands(program, cmds):
    for cmd in cmds:
        program.set_input_str("{}\n".format(cmd))
        program.output = []
        if run_until_input(program):
            return (True, program.output_as_str())
        assert len(program.input) == 0
    return (False, program.output_as_str())


program = Program(memory, ())
run_until_input(program)

execute_commands(program, [
    "south", "south", "take spool of cat6",
    "west", "take space heater",
    "south", "take shell", "north",
    "north", "take weather machine",
    "west", "south", "east", "take candy cane", "west",
    "south", "take space law space brochure", "north",
    "north", "east", "south", "east", "east", "south",
    "take hypercube", "south", "south"
])
inventory = ["weather machine", "shell", "candy cane", "hypercube", "space law space brochure", "space heater", "spool of cat6"]
drop_cmds = ["drop {}".format(item) for item in inventory]
execute_commands(program, drop_cmds)
valid_combinations = []

for l in range(1, len(inventory) + 1):
    combinations = list(itertools.combinations(inventory, l))
    for comb in combinations:
        prog_copy = program.copy()
        execute_commands(prog_copy, ["take {}".format(item) for item in comb] + ["east"])
        if "Alert!" not in prog_copy.output_as_str():
            print(prog_copy.output_as_str())
            valid_combinations.append(combinations)

print(valid_combinations)

while True:
    end = run_until_input(program)
    print(program.output_as_str())
    if end:
        break
    program.output = []
    cmd = input().strip()
    program.set_input_str("{}\n".format(cmd))

"""
(S, S) -> cat6
    (W) -> space heater
        (S) -> shell
        (N) -> weather machine
            (WS)
                (E) -> candy cane
                (S) -> space law space brochure
    (ES) -> hypercube
        (SSE) -> checkpoint
"""
