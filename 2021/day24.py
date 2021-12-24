import dataclasses
import random
from typing import Dict, List, Tuple, Union

import tqdm


@dataclasses.dataclass
class ALU:
    registers: List[int] = dataclasses.field(default_factory=lambda: [0] * 4)

    def is_valid(self) -> bool:
        return self.registers[self.reg_index("z")] == 0

    def reg_index(self, reg: str) -> int:
        return "wxyz".index(reg)

    def get_reg(self, reg: str) -> int:
        return self.registers[self.reg_index(reg)]

    def set_reg(self, reg: str, value: int):
        self.registers[self.reg_index(reg)] = value

    def resolve(self, value: str) -> int:
        if value in "wxyz":
            return self.get_reg(value)
        return int(value)


Bounds = Tuple[int, int]


@dataclasses.dataclass
class Expr:
    def bounds(self) -> Bounds:
        raise NotImplementedError

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        return self


@dataclasses.dataclass
class Constant(Expr):
    value: int

    def bounds(self) -> Bounds:
        return (self.value, self.value)

    def __repr__(self):
        return str(self.value)


@dataclasses.dataclass
class Add(Expr):
    left: Expr
    right: Expr

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        l, r = self.left.constprop(input, output), self.right.constprop(input, output)
        if isinstance(l, Constant) and l.value == 0:
            return r
        if isinstance(r, Constant) and r.value == 0:
            return l
        if isinstance(l, Constant) and isinstance(r, Constant):
            return Constant(l.value + r.value)

        return Add(left=l, right=r)

    def bounds(self) -> Bounds:
        (a, b) = self.left.bounds()
        (x, y) = self.right.bounds()
        return (a + x, b + y)

    def __repr__(self):
        return f"({self.left} + {self.right})"


@dataclasses.dataclass
class Mod(Expr):
    left: Expr
    right: Expr

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        l, r = self.left.constprop(input, output), self.right.constprop(input, output)
        if isinstance(l, Constant) and isinstance(r, Constant):
            return Constant(l.value % r.value)

        return Mod(left=l, right=r)

    def bounds(self) -> Bounds:
        # (a, b) = self.left.bounds()
        (x, y) = self.right.bounds()
        assert x == y
        assert isinstance(self.right, Constant)
        # return (a % x, b % y)
        return (0, x - 1)

    def __repr__(self):
        return f"({self.left} % {self.right})"


@dataclasses.dataclass
class Mul(Expr):
    left: Expr
    right: Expr

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        l, r = self.left.constprop(input, output), self.right.constprop(input, output)
        if isinstance(l, Constant) and isinstance(r, Constant):
            return Constant(l.value * r.value)
        if isinstance(r, Constant):
            if r.value == 1:
                return l
            if r.value == 0:
                return Constant(0)
        elif isinstance(l, Constant):
            if l.value == 1:
                return r
            if l.value == 0:
                return Constant(0)
        return Mul(left=l, right=r)

    def bounds(self) -> Bounds:
        # (a, b) = self.left.bounds()
        (x, y) = self.right.bounds()
        assert x == y
        assert isinstance(self.right, Constant)
        # return (a % x, b % y)
        return (0, x - 1)

    def __repr__(self):
        return f"({self.left} * {self.right})"


@dataclasses.dataclass
class Div(Expr):
    left: Expr
    right: Expr

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        l, r = self.left.constprop(input, output), self.right.constprop(input, output)
        if isinstance(l, Constant) and isinstance(r, Constant):
            return Constant(int(l.value / r.value))
        if isinstance(r, Constant):
            if r.value == 1:
                return l
        return Div(left=l, right=r)

    def bounds(self) -> Bounds:
        (a, b) = self.left.bounds()
        (x, y) = self.right.bounds()
        return (int(a / y), int(b / x))

    def __repr__(self):
        return f"({self.left} / {self.right})"


@dataclasses.dataclass
class Input(Expr):
    index: int

    def bounds(self) -> Bounds:
        return (1, 9)

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        if self.index in input:
            return Constant(input[self.index])
        return self

    def __repr__(self):
        return f"w{self.index}"


@dataclasses.dataclass
class Equal(Expr):
    left: Expr
    right: Expr

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        l, r = self.left.constprop(input, output), self.right.constprop(input, output)
        if isinstance(l, Constant) and isinstance(r, Constant):
            v = l.value == r.value
            return Constant(1 if v else 0)

        (a, b) = l.bounds()
        (x, y) = r.bounds()
        if b < x or y < a:
            return Constant(0)
        elif a == b and x == y and a == y:
            return Constant(1)
        return Equal(left=l, right=r)

    def bounds(self) -> Bounds:
        (a, b) = self.left.bounds()
        (x, y) = self.right.bounds()
        if b < x or y < a:
            return (0, 0)
        return (0, 1)

    def __repr__(self):
        return f"({self.left} == {self.right})"


@dataclasses.dataclass
class Output(Expr):
    index: int
    expr: Expr

    def constprop(self, input: Dict[int, int], output=None) -> "Expr":
        expr = self.expr.constprop(input, output)
        if output and self.index in output:
            return expr
        return Output(index=self.index, expr=expr)

    def bounds(self) -> Bounds:
        return self.expr.bounds()

    def __repr__(self):
        return f"z{self.index}"


def build_ast(commands: List[str]) -> List[Expr]:
    input_id = 0
    exprs = [Constant(0), Constant(0), Constant(0), Constant(0)]
    alu = ALU()

    def resolve(value: str) -> Expr:
        if value in "wxyz":
            return exprs[alu.reg_index(value)]
        return Constant(int(value))

    for command in commands:
        cmd = command.split()
        if cmd[0] == "inp":
            exprs[alu.reg_index(cmd[1])] = Input(input_id)
            print(f"z[{input_id}] = {exprs[3]}")

            # x = {0: 1, 1: 1, 2: 1, 3: 4, 4: 4, 5: 1}
            x = {0: 9, 1: 9, 2: 9, 3: 2, 4: 4, 5: 1}
            # print(exprs[3].constprop({}, set(range(15))))
            # print(exprs[3].constprop(x))
            # print(exprs[3].constprop(x, set(range(15))))
            # print()

            exprs[3] = Output(index=input_id, expr=exprs[3])
            input_id += 1
            if input_id == TO_ID + 1:
                break
            # if input_id > 5:
            #     exprs[3] = exprs[3].constprop(x)
            # if input_id > 5:
            #     exit()
        else:
            a, b = cmd[1:]
            if cmd[0] == "add":
                exprs[alu.reg_index(a)] = Add(resolve(a), resolve(b)).constprop({})
            elif cmd[0] == "mul":
                exprs[alu.reg_index(a)] = Mul(resolve(a), resolve(b)).constprop({})
            elif cmd[0] == "div":
                exprs[alu.reg_index(a)] = Div(resolve(a), resolve(b)).constprop({})
            elif cmd[0] == "mod":
                exprs[alu.reg_index(a)] = Mod(resolve(a), resolve(b)).constprop({})
            elif cmd[0] == "eql":
                exprs[alu.reg_index(a)] = Equal(resolve(a), resolve(b)).constprop({})
            else:
                assert False
    exprs = [expr.constprop({}) for expr in exprs]
    print(f"z[{input_id}] = {exprs[3]}")
    return exprs


# I0: [w0, 1, w0 + 14, w0 + 14]
# I1: [w1, 1, w1 + 8, (w0 + 14) * 26 + w1 + 8]
# I2: [w2, 1, w2 + 5, ((w0 + 14) * 26 + w1 + 8) * 26 + w2 + 5]

def execute(input: str, commands: List[str]) -> ALU:
    alu = ALU()
    assert len(input) == 14
    input = list(reversed([int(v) for v in input]))

    for command in commands:
        cmd = command.split()
        if cmd[0] == "inp":
            alu.set_reg(cmd[1], input.pop())
        else:
            a, b = cmd[1:]
            if cmd[0] == "add":
                res = alu.resolve(a) + alu.resolve(b)
                alu.set_reg(a, res)
            elif cmd[0] == "mul":
                res = alu.resolve(a) * alu.resolve(b)
                alu.set_reg(a, res)
            elif cmd[0] == "div":
                res = int(alu.resolve(a) / alu.resolve(b))
                alu.set_reg(a, res)
            elif cmd[0] == "mod":
                res = alu.resolve(a) % alu.resolve(b)
                alu.set_reg(a, res)
            elif cmd[0] == "eql":
                res = alu.resolve(a) == alu.resolve(b)
                if res:
                    alu.set_reg(a, 1)
                else:
                    alu.set_reg(a, 0)
            else:
                assert False
    return alu


def random_input() -> str:
    v = ""
    for _ in range(14):
        v += str(random.randrange(1, 10))
    return v


def input_to_dict(input: Union[str, int]) -> Dict[int, int]:
    input = str(input)
    return {i: int(v) for (i, v) in enumerate(str(input))}


def run_program(input: str) -> List[int]:
    input = input.replace("_", "")
    w = [int(v) for v in input]
    z = [-1] * 15

    z[0] = 0
    z[1] = ((z[0] * 26) + (w[0] + 14))
    z[2] = ((z[1] * 26) + (w[1] + 8))
    z[3] = ((z[2] * 26) + (w[2] + 5))
    z[4] = (((int(z[3] / 26)) * ((25 * (((z[3] % 26) == w[3]) == 0)) + 1)) + (
                (w[3] + 4) * (((z[3] % 26) == w[3]) == 0)))
    z[5] = ((z[4] * 26) + (w[4] + 10))
    z[6] = (((int(z[5] / 26)) * ((25 * ((((z[5] % 26) + -13) == w[5]) == 0)) + 1)) + (
                (w[5] + 13) * ((((z[5] % 26) + -13) == w[5]) == 0)))
    z[7] = ((z[6] * 26) + (w[6] + 16))
    z[8] = (((int(z[7] / 26)) * ((25 * ((((z[7] % 26) + -9) == w[7]) == 0)) + 1)) + (
                (w[7] + 5) * ((((z[7] % 26) + -9) == w[7]) == 0)))
    z[9] = ((z[8] * 26) + (w[8] + 6))
    z[10] = ((z[9] * 26) + (w[9] + 13))
    z[11] = (((int(z[10] / 26)) * ((25 * ((((z[10] % 26) + -14) == w[10]) == 0)) + 1)) + (
                (w[10] + 6) * ((((z[10] % 26) + -14) == w[10]) == 0)))
    z[12] = (((int(z[11] / 26)) * ((25 * ((((z[11] % 26) + -3) == w[11]) == 0)) + 1)) + (
                (w[11] + 7) * ((((z[11] % 26) + -3) == w[11]) == 0)))
    z[13] = (((int(z[12] / 26)) * ((25 * ((((z[12] % 26) + -2) == w[12]) == 0)) + 1)) + (
                (w[12] + 13) * ((((z[12] % 26) + -2) == w[12]) == 0)))
    z[14] = (((int(z[13] / 26)) * ((25 * ((((z[13] % 26) + -14) == w[13]) == 0)) + 1)) + (
                (w[13] + 3) * ((((z[13] % 26) + -14) == w[13]) == 0)))
    return z


commands = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        commands.append(line)

# w0 + w1 + w2 + 1 != w3

# z0 = 0
# z1 = w0 + 14
# z2 = w0 + w1 + 22
# z3 = w0 + w1 + w2 + 1
# z4 = w0 + w1 + w2 + w3 + 5
# z5 = w0 + w1 + w2 + w3 + w4 + 15
# z6 = w0 + w1 + w2 + w3 + w4 + w5 + 2 # TODO

TO_ID = 14
ast = build_ast(commands)

#                 01234567890123
# zs = run_program("93499629698999")

#                 01234567890123
zs = run_program("11164118121471")
for (index, z) in enumerate(zs):
    print(index, z)
exit()

# 93499618698999 too low

# input = "29496318116953"
# input = "1127521882149"
# data = input_to_dict(input)

data = {
    0: 9,
    1: 9,
    2: 9,
    3: 6,
    4: 7,
    5: 4,
    6: 1,
    7: 8,
    8: 9,
    9: 2,
    10: 1,
    11: 4,
    12: 9,
    13: 8
}

ret = ast[3].constprop(data, set(range(14)))
print(ret)
exit()


for w0 in range(1, 10):
    for w1 in range(1, 10):
        for w2 in range(1, 10):
            d = dict(data)
            i, j, k = random.randrange(0, 14), random.randrange(0, 14), random.randrange(0, 14)
            d[0] = i
            d[1] = j
            d[2] = k
            # d[2] = w2
            # del d[13]
            # r = ast[3].constprop(d)
            # print(r)
            # print(r.constprop({13: 8}))
            # key = (w0, w1, w2)
            key = (i, j, k)
            print(key, ast[3].constprop(d))
exit()


execute(input, commands)

for value in tqdm.tqdm(range(99999999999999, 0, -1)):
    input = str(value)
    if "0" in input:
        continue
    alu = execute(input, commands)
    if alu.is_valid():
        print(value)
