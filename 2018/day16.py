with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]


def select(regs, index, imm):
    if imm:
        return index
    else:
        return regs[index]


def add(reg, a, b, c, imm):
    ret = list(reg)
    ret[c] = ret[a] + select(ret, b, imm)
    return ret


def mul(reg, a, b, c, imm):
    ret = list(reg)
    ret[c] = ret[a] * select(ret, b, imm)
    return ret


def band(reg, a, b, c, imm):
    ret = list(reg)
    ret[c] = ret[a] & select(ret, b, imm)
    return ret


def bor(reg, a, b, c, imm):
    ret = list(reg)
    ret[c] = ret[a] | select(ret, b, imm)
    return ret


def setinst(reg, a, b, c, imm):
    ret = list(reg)
    ret[c] = select(ret, a, imm)
    return ret


def gt(reg, a, b, c, imm):
    ret = list(reg)
    a = select(ret, a, 1 if imm == 0 else 0)
    b = select(ret, b, 1 if imm == 1 else 0)
    ret[c] = 1 if a > b else 0
    return ret


def eq(reg, a, b, c, imm):
    ret = list(reg)
    a = select(ret, a, 1 if imm == 0 else 0)
    b = select(ret, b, 1 if imm == 1 else 0)
    ret[c] = 1 if a == b else 0
    return ret


def parse_line(l):
    return list(map(int, l.rstrip("]")[l.index("[") + 1:].split(",")))


instructions = {
    'addr': lambda r, i: add(r, *i, 0),
    'addi': lambda r, i: add(r, *i, 1),
    'mulr': lambda r, i: mul(r, *i, 0),
    'muli': lambda r, i: mul(r, *i, 1),
    'banr': lambda r, i: band(r, *i, 0),
    'bani': lambda r, i: band(r, *i, 1),
    'borr': lambda r, i: bor(r, *i, 0),
    'bori': lambda r, i: bor(r, *i, 1),
    'setr': lambda r, i: setinst(r, *i, 0),
    'seti': lambda r, i: setinst(r, *i, 1),
    'gtir': lambda r, i: gt(r, *i, 0),
    'gtri': lambda r, i: gt(r, *i, 1),
    'gtrr': lambda r, i: gt(r, *i, 2),
    'eqir': lambda r, i: eq(r, *i, 0),
    'eqri': lambda r, i: eq(r, *i, 1),
    'eqrr': lambda r, i: eq(r, *i, 2)
}

opcodes = {}

i = 0
multi = 0
while i < len(lines):
    before = parse_line(lines[i])
    inst = list(map(int, lines[i + 1].split(" ")))
    after = parse_line(lines[i + 2])

    valid = []
    for instruction in instructions:
        if instructions[instruction](before, inst[1:]) == after:
            valid.append(instruction)
    for v in valid:
        opcodes.setdefault(v, set()).add(inst[0])
    i += 4
print(opcodes)
reverse = {}
for o in opcodes:
    for v in opcodes[o]:
        reverse.setdefault(v, set()).add(o)


def assign(opcode, assignments):
    if opcode >= len(reverse):
        return True

    for poss in reverse[opcode]:
        if poss not in assignments:
            assignments[poss] = opcode
            if assign(opcode + 1, assignments):
                return True
            del assignments[poss]

    return False

assignments = {}
res = assign(0, assignments)
opcodes = dict((v, k) for (k, v) in assignments.items())

regs = [0] * 4
with open("input2.txt", "r") as f:
    for line in f:
        inst = list(map(int, line.strip().split(" ")))
        regs = instructions[opcodes[inst[0]]](regs, inst[1:])
print(regs[0])
