import traceback


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


def evaluate(program):
    try:
        while True:
            opcode = program.memread(program.pc) % 100
            (param_count, fn) = instructions[opcode]
            modes = list(int(c) for c in str(program.memread(program.pc) // 100)[::-1])
            modes += [0] * (param_count - len(modes))
            args = tuple(Arg(v, m, program) for (v, m) in
                         zip((program.memread(a) for a in
                              range(program.pc + 1, program.pc + 1 + param_count)), modes))
            ret = fn(program, args)
            if ret is True:
                break
            elif isinstance(ret, int):
                program.pc = ret
            else:
                program.pc += 1 + param_count
    except:
        traceback.print_exc()
    return program


with open("input.txt") as f:
    memory = tuple(int(v) for v in f.read().strip().split(","))

program = Program(memory, (2, ))
evaluate(program)
print(program.output)
