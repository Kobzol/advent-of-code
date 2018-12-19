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
    data = l.split(" ")
    return (data[0], list(map(int, data[1:])))


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
    'eqrr': lambda r, i: eq(r, *i, 2),
    'nop': lambda r, i: list(r)
}

lines = lines[1:]
regs = [0] * 6
regs[0] = 1
ip = 0
ipindex = 2
while 0 <= ip < len(lines):
    regs[ipindex] = ip
    inst, params = parse_line(lines[ip])
    regs = instructions[inst](regs, params)
    ip = regs[ipindex]
    ip += 1
print(regs[0])

"""
R2 += 16
R4 = 1
R5 = 1
R1 = R4 * R5
R1 = R1 == R3
R2 += R1
R2 += 1
R0 = R4
R5 += 1
R1 = R5 > R3
R2 += R1
R2 = 6
R4 += 1
R1 = R4 > R3
R2 += R1
R2 = R1
R2 *= R2
R3 += 3
R3 *= R3
R3 *= R2
R3 *= 3
R1 += 1
R1 *= R2
R1 += 1
R3 += R1
R2 += R0
R2 = 0
R1 = R2
R1 *= R2
R1 += R2
R1 *= R2
R1 *= 1
R1 *= R2
R3 += R1
R0 = 0
R2 = 0
"""
