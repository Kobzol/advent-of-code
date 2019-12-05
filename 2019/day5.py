import traceback


class Program:
    def __init__(self, memory, input):
        self.memory = list(memory)
        self.input = list(input[::-1])
        self.output = []

    def read(self):
        return self.input.pop()

    def write(self, c):
        self.output.append(c)


class Arg:
    def __init__(self, val, mode, program):
        self.val = val
        self.mode = mode
        self.program = program

    def eval(self):
        if self.mode == 0:
            return self.program.memory[self.val]
        elif self.mode == 1:
            return self.val
        else:
            assert False


def stop(program, args):
    return True


def add(program, args):
    program.memory[args[2].val] = args[0].eval() + args[1].eval()


def mul(program, args):
    program.memory[args[2].val] = args[0].eval() * args[1].eval()


def read(program, args):
    program.memory[args[0].val] = program.read()


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
    program.memory[args[2].val] = val


def equals(program, args):
    val = 0
    if args[0].eval() == args[1].eval():
        val = 1
    program.memory[args[2].val] = val


instructions = {
    99: (0, stop),
    1: (3, add),
    2: (3, mul),
    3: (1, read),
    4: (1, write),
    5: (2, jumpiftrue),
    6: (2, jumpiffalse),
    7: (3, lessthan),
    8: (3, equals)
}


def evaluate(memory, input=(), pc=0):
    program = Program(memory, input)

    try:
        while True:
            opcode = program.memory[pc] % 100
            (param_count, fn) = instructions[opcode]
            modes = list(int(c) for c in str(program.memory[pc] // 100)[::-1])
            modes += [0] * (param_count - len(modes))
            args = tuple(Arg(v, m, program) for (v, m) in zip(program.memory[pc+1:pc+1+param_count], modes))
            # print(opcode, modes, program.memory[pc+1:pc+1+param_count], args)
            ret = fn(program, args)
            if ret is True:
                break
            elif isinstance(ret, int):
                pc = ret
            else:
                pc += 1 + param_count
    except:
        traceback.print_exc()
    return program


with open("input.txt") as f:
    memory = tuple(int(v) for v in f.read().split(","))
    p = evaluate(memory, (5, ))
    print(p.memory, p.output)
