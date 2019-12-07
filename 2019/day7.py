import itertools
import traceback


class Program:
    def __init__(self, memory, input):
        self.memory = list(memory)
        self.input = list(input[::-1])
        self.output = []
        self.pc = 0

    def add_input(self, c):
        self.input = [c] + self.input

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


def evaluate(program):
    try:
        while True:
            opcode = program.memory[program.pc] % 100
            (param_count, fn) = instructions[opcode]
            modes = list(int(c) for c in str(program.memory[program.pc] // 100)[::-1])
            modes += [0] * (param_count - len(modes))
            args = tuple(Arg(v, m, program) for (v, m) in
                         zip(program.memory[program.pc + 1:program.pc + 1 + param_count], modes))
            # print(opcode, modes, program.memory[pc+1:pc+1+param_count], args)
            ret = fn(program, args)
            if ret is True:
                break
            elif isinstance(ret, int):
                program.pc = ret
            else:
                program.pc += 1 + param_count

            if opcode == 4:
                return (program, False)
    except:
        traceback.print_exc()
    return (program, True)


perms = itertools.permutations(range(5, 10))
memory = [3,8,1001,8,10,8,105,1,0,0,21,34,43,60,81,94,175,256,337,418,99999,3,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,102,3,9,9,4,9,99,3,9,102,4,9,9,1001,9,2,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99]


def run_simulation(memory, permutation):
    amplifiers = [Program(memory, [p]) for p in permutation]
    halted = 0

    last_output = 0
    while True:
        for amplifier in amplifiers:
            amplifier.add_input(last_output)
            _, end = evaluate(amplifier)
            if end:
                halted += 1
            last_output = amplifier.output[-1]
        if halted == len(amplifiers):
            break

    return amplifiers[-1].output[-1]


maximum = None
max_perm = None
for perm in perms:
    ret = run_simulation(memory, perm)
    if maximum is None or ret > maximum:
        maximum = ret
        max_perm = perm
print(maximum, max_perm)
