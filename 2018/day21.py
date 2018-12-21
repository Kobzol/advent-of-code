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


def simulate(r0=0):
    regs = [r0, 0, 0, 0, 0, 0]
    counter = {}

    count = 6
    while True:
        regs[4] = regs[5] | 65536; count += 1
        regs[5] = 13159625; count += 1

        while True:
            regs[3] = regs[4] & 255 ; count += 1
            regs[5] += regs[3]; count += 1
            regs[5] %= 16777216; count += 1
            regs[5] *= 65899; count += 1
            regs[5] %= 16777216; count += 1
            count += 1
            if 256 > regs[4]:
                if regs[5] not in counter:
                    counter[regs[5]] = count
                print(len(counter), min(counter), max(counter))

                maxcount = 0
                regkey = 0
                for (k, v) in counter.items():
                    if v > maxcount:
                        maxcount = v
                        regkey = k
                print(regkey)

                regs[3] = 1 if regs[5] == regs[0] else 0
                count += 1
                if regs[3] == 1:
                    count += 1
                    return count
                else:
                    break
            regs[3] = regs[4] // 256; count += 1
            regs[4] = regs[3]; count += 1


simulate(0)
