from collections import deque


def deal_into(deck):
    deck.reverse()
    return deck


def cut(deck, n):
    d = list(deck)
    return deque(d[n:] + d[:n])


def deal_with(deck, n):
    new = deque(deck)
    target = 0
    for i in range(len(new)):
        new[target] = deck[i]
        target = (target + n) % len(deck)
    return new


commands = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("deal with increment "):
            commands.append(("deal with", int(line[20:])))
        elif line.startswith("deal into"):
            commands.append(("deal into", None))
        elif line.startswith("cut "):
            commands.append(("cut", int(line[4:])))


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def invert_position(pos, increment, size):
    _, x0, _ = xgcd(increment, size)
    return (pos * x0) % size


def solve_position(cmd_index, position, size):
    if cmd_index < 0:
        return position
    cmd, arg = commands[cmd_index]
    if cmd == "deal into":
        position = (size - 1) - position
    elif cmd == "deal with":
        position = invert_position(position, arg, size)
    else:
        if arg >= 0:
            if position < (size - arg):
                position += arg
            else:
                position -= (size - arg)
        else:
            arg = abs(arg)
            if position < arg:
                position += (size - arg)
            else:
                position -= arg
    return solve_position(cmd_index - 1, position, size)


def solve(pos):
    return solve_position(len(commands) - 1, pos, size)


size = 119315717514047
iter_count = 101741582076661


offset = 0
increment = 1


def inv(n):
    return pow(n, size - 2, size)


for cmd, arg in commands:
    if cmd == "deal into":
        increment *= -1
        increment = increment % size
        offset += increment
        offset = offset % size
    elif cmd == "cut":
        offset += increment * arg
        offset = offset % size
    else:
        increment *= inv(arg)
        increment = increment % size


offset_diff, increment_mul = (offset % size, increment % size)
print(offset, increment)
print(offset_diff, increment_mul)

f_increment = pow(increment_mul, iter_count, size)
f_offset = (offset_diff * ((1 - f_increment) % size) * inv(1 - increment_mul)) % size

print(f_offset, f_increment)
print((f_offset + f_increment * 2020) % size)

# 81455262316689 too high
# 55625704785658 too high
# 5699251196658 too low
# 13224103523662
