import dataclasses
from typing import Dict, Union


@dataclasses.dataclass
class Plus:
    def evaluate(self, a: int, b: int) -> int:
        return a + b

    def find_other(self, target: int, a: int, lhs: bool) -> int:
        return target - a


@dataclasses.dataclass
class Minus:
    def evaluate(self, a: int, b: int) -> int:
        return a - b

    def find_other(self, target: int, a: int, lhs: int) -> int:
        if lhs:
            return a - target
        else:
            return a + target


@dataclasses.dataclass
class Mul:
    def evaluate(self, a: int, b: int) -> int:
        return a * b

    def find_other(self, target: int, a: int, lhs: int) -> int:
        return target // a


@dataclasses.dataclass
class Div:
    def evaluate(self, a: int, b: int) -> int:
        return a // b

    def find_other(self, target: int, a: int, lhs: int) -> int:
        if lhs:
            return a // target
        else:
            return a * target


SymBinOp = Union[Plus, Minus, Mul, Div]


@dataclasses.dataclass
class OpYell:
    number: int


@dataclasses.dataclass
class OpCompute:
    a: str
    b: str
    op: SymBinOp


Op = Union[OpYell, OpCompute]


@dataclasses.dataclass
class SymOperation:
    a: "Sym"
    b: "Sym"
    op: SymBinOp


@dataclasses.dataclass
class SymValue:
    value: int


@dataclasses.dataclass
class UnknownValue:
    pass


Sym = Union[SymOperation, SymValue, UnknownValue]


@dataclasses.dataclass
class Monkey:
    id: int
    name: str
    op: Op

    def compute(self, monkeys: Dict[str, "Monkey"]) -> int:
        if isinstance(self.op, OpYell):
            return self.op.number
        elif isinstance(self.op, OpCompute):
            a = monkeys[self.op.a].compute(monkeys)
            b = monkeys[self.op.b].compute(monkeys)
            return self.op.op.evaluate(a, b)
        else:
            assert False

    def sym_compute(self, monkeys: Dict[str, "Monkey"]) -> Sym:
        if self.name == "humn":
            return UnknownValue()

        if isinstance(self.op, OpYell):
            return SymValue(value=self.op.number)
        elif isinstance(self.op, OpCompute):
            a = monkeys[self.op.a].sym_compute(monkeys)
            b = monkeys[self.op.b].sym_compute(monkeys)

            if isinstance(a, SymValue) and isinstance(b, SymValue):
                return SymValue(value=self.op.op.evaluate(a.value, b.value))
            else:
                return SymOperation(a=a, b=b, op=self.op.op)

    def reaches_unknown(self, monkeys: Dict[str, "Monkey"]) -> bool:
        if self.name == "humn":
            return True

        if isinstance(self.op, OpYell):
            return False
        elif isinstance(self.op, OpCompute):
            return monkeys[self.op.a].reaches_unknown(monkeys) or monkeys[
                self.op.b].reaches_unknown(monkeys)


def evaluate_sym(tree: Sym, unknown_value: int) -> int:
    if isinstance(tree, UnknownValue):
        return unknown_value
    elif isinstance(tree, SymOperation):
        a = evaluate_sym(tree.a, unknown_value)
        b = evaluate_sym(tree.b, unknown_value)
        return tree.op.evaluate(a, b)
    elif isinstance(tree, SymValue):
        return tree.value
    else:
        assert False


def find_unknown(tree: Sym, target: int) -> int:
    if isinstance(tree, UnknownValue):
        return target
    elif isinstance(tree, SymOperation):
        assert (isinstance(tree.a, SymValue) or isinstance(tree.b, SymValue))

        (fixed, unknown) = (tree.a, tree.b)
        lhs = True
        if isinstance(tree.b, SymValue):
            (fixed, unknown) = (tree.b, tree.a)
            lhs = False

        new_target = tree.op.find_other(target, a=fixed.value, lhs=lhs)
        return find_unknown(unknown, new_target)
    else:
        assert False


monkeys = {}
ops = {
    "+": Plus,
    "-": Minus,
    "*": Mul,
    "/": Div
}
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        name, rest = line.split(": ")
        if " " in rest:
            a, op, b = rest.split(" ")
            op = OpCompute(a=a, b=b, op=ops[op]())
        else:
            value = int(rest)
            op = OpYell(number=value)
        assert name not in monkeys
        monkeys[name] = Monkey(name=name, id=len(monkeys), op=op)

a = monkeys["root"].op.a
b = monkeys["root"].op.b

(is_fixed, has_unknown) = (a, b)
if monkeys[a].reaches_unknown(monkeys):
    (is_fixed, has_unknown) = (b, a)

assert monkeys[a].reaches_unknown(monkeys) != monkeys[b].reaches_unknown(monkeys)

sym_tree = monkeys[has_unknown].sym_compute(monkeys)
target = find_unknown(sym_tree, monkeys[is_fixed].compute(monkeys))

print(target)
monkeys["humn"].op = OpYell(number=target)
print(monkeys[is_fixed].compute(monkeys), monkeys[has_unknown].compute(monkeys))
print(monkeys[a].compute(monkeys) == monkeys[b].compute(monkeys))
