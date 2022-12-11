import collections
import dataclasses
import math
import operator
from functools import reduce
from typing import Callable, List, Optional

from tqdm import tqdm


@dataclasses.dataclass
class Monkey:
    items: collections.deque[int]
    operation: Callable[[int], int]
    test_value: int
    target_true: int
    target_false: int
    inspected_count: int = 0

    def hash(self) -> str:
        return "-".join(str(v) for v in self.items)

    def turn(self, monkeys: List["Monkey"], nominator: int):
        items = list(self.items)
        self.items.clear()

        for item in items:
            self.inspected_count += 1
            new_value = self.operation(item)
            # new_value //= 3
            new_value %= nominator
            if new_value % self.test_value == 0:
                target = self.target_true
            else:
                target = self.target_false
            assert monkeys[target] is not self
            monkeys[target].items.append(new_value)


lines = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        lines.append(line)


def iter_monkey_lines():
    monkey_lines = []
    for line in lines:
        if line == "":
            yield monkey_lines
            monkey_lines = []
        else:
            monkey_lines.append(line)
    if monkey_lines:
        yield monkey_lines


def parse_monkey(lines: List[str]) -> Monkey:
    items = [int(v) for v in lines[1][len("Starting items: "):].split(",")]
    ops = lines[2].split(" ")[-2:]

    def operation(old: int):
        op = operator.add if ops[0] == "+" else operator.mul
        rhs = int(ops[1]) if ops[1] != "old" else old
        return op(old, rhs)

    test_value = int(lines[3].split(" ")[-1])
    target_true = int(lines[4].split(" ")[-1])
    target_false = int(lines[5].split(" ")[-1])

    return Monkey(
        items=collections.deque(items),
        operation=operation,
        test_value=test_value,
        target_true=target_true,
        target_false=target_false
    )

monkeys = [parse_monkey(m) for m in iter_monkey_lines()]
nominator = reduce(lambda a, b: a * b, [m.test_value for m in monkeys], 1)
print(nominator)

round_hashes = set()
for round in tqdm(range(10000)):
    # hashes = "x".join(m.hash() for m in monkeys)
    # assert hashes not in round_hashes
    # round_hashes.add(hashes)

    for (index, monkey) in enumerate(monkeys):
        # if index == 0:
        #     start = monkey.inspected_count
        monkey.turn(monkeys, nominator=nominator)
        # if index == 0:
        #     print(monkey.inspected_count - start)
    # print(monkeys)
    # break

for monkey in monkeys:
    print(monkey.inspected_count)

monkeys = sorted(monkeys, key=lambda m: m.inspected_count, reverse=True)
monkey_business = monkeys[0].inspected_count * monkeys[1].inspected_count
print(monkey_business)

# 11989302727 too high
