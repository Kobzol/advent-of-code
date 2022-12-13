import dataclasses
import itertools
from functools import cmp_to_key
from typing import Any, List


class TriState:
    Lower = -1
    Same = 0
    Upper = 1


def compare(a, b) -> int:
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return TriState.Lower
        elif a > b:
            return TriState.Upper
        return TriState.Same
    if isinstance(a, list) and isinstance(b, list):
        iterated = 0
        for (x, y) in zip(a, b):
            state = compare(x, y)
            if state != TriState.Same:
                return state
            iterated += 1
        if iterated < len(b):
            return TriState.Lower
        if iterated < len(a):
            return TriState.Upper
        return TriState.Same
    if isinstance(a, int):
        a = [a]
    elif isinstance(b, int):
        b = [b]
    return compare(a, b)


@dataclasses.dataclass
class Pair:
    left: List[Any]
    right: List[Any]

    def in_order(self) -> int:
        return compare(self.left, self.right)


def linearize(line: str):
    root = None
    stack = []
    num = None
    for char in line:
        if char == "[":
            assert num is None
            if root is None:
                root = []
                item = root
            else:
                stack[-1].append([])
                item = stack[-1][-1]
            stack.append(item)
        elif char == "]":
            if num is not None:
                stack[-1].append(num)
                num = None
            stack.pop()
        elif char == ",":
            if num is not None:
                stack[-1].append(num)
                num = None
        elif char.isdigit():
            if num is None:
                num = 0
            num *= 10
            num += int(char)
    assert root is not None
    return root


lines = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)

pairs = []
for index in range(0, len(lines), 2):
    left = lines[index]
    right = lines[index + 1]
    pair = Pair(
        left=list(linearize(left)),
        right=list(linearize(right))
    )
    a = str(pair.left).replace(" ", "")
    assert a == left
    b = str(pair.right).replace(" ", "")
    assert b == right
    pairs.append(pair)

divider_a = [[2]]
divider_b = [[6]]

pairs.append(Pair(left=divider_a, right=divider_b))

items = list(itertools.chain.from_iterable([p.left, p.right] for p in pairs))
items = sorted(items, key=cmp_to_key(compare))

print((items.index(divider_a) + 1) * (items.index(divider_b) + 1))
