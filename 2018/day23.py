import z3

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

bots = []

for line in lines:
    pos = list(map(int, line[line.index("pos=<") + 5:line.index(">")].split(",")))
    radius = int(line[line.index("r=") + 2:])
    bots.append((tuple(pos), radius))

bots = sorted(bots, key=lambda b: b[1], reverse=True)


def dist(a, b):
    return sum(abs(x-y) for (x, y) in zip(a, b))


def inrange(pos, bot):
    return dist(pos, bot[0]) <= bot[1]


def botcount(pos):
    return len(list(bot for bot in bots if inrange(pos, bot)))


x, y, z = z3.Ints('x y z')

s = z3.Solver()
o = z3.Optimize()


def absolute(x):
    return z3.If(x >= 0, x, -x)


for (pos, radius) in bots:
    a = absolute(pos[0] - x)
    b = absolute(pos[1] - y)
    c = absolute(pos[2] - z)
    o.add_soft((a + b + c) <= radius, 1)

o.minimize(x)
o.minimize(y)
o.minimize(z)
print(o.check())

model = o.model()
pos = model.get_interp(x).as_long(), model.get_interp(y).as_long(), model.get_interp(z).as_long()

print(pos, dist((0, 0, 0), pos))
