import dataclasses
import itertools
import math
from typing import Optional, Tuple


@dataclasses.dataclass
class Number:
    def __add__(self, other):
        return Pair(left=self, right=other)

    def magnitude(self) -> int:
        raise NotImplementedError

    def leftmost(self, level=0):
        yield (self, level)

    def rightmost(self, level=0):
        yield (self, level)

    def copy(self) -> "Number":
        raise NotImplementedError

    def reduce(self) -> "Number":
        root = self
        while True:
            found = False
            for (number, level) in root.leftmost():
                if isinstance(number, Pair) and level == 4:  # level >= 4
                    number.explode()
                    found = True
                    break
            if found:
                continue
            for (number, level) in root.leftmost():
                if isinstance(number, Literal) and number.value >= 10:
                    number.split()
                    found = True
                    break
            if not found:
                break
        return root


@dataclasses.dataclass
class Literal(Number):
    value: int
    parent: Optional["Number"] = None

    def split(self) -> "Number":
        divided = self.value / 2
        l = math.floor(divided)
        r = math.ceil(divided)
        pair = Pair(left=Literal(value=l), right=Literal(value=r), parent=self.parent)
        if self.parent:
            self.parent.replace(self, pair)
        return pair

    def magnitude(self) -> int:
        return self.value

    def copy(self) -> "Number":
        return Literal(value=self.value)

    def __repr__(self):
        return str(self.value)


@dataclasses.dataclass
class Pair(Number):
    left: Number
    right: Number
    parent: Optional["Number"] = None

    def __post_init__(self):
        self.left.parent = self
        self.right.parent = self

    def __repr__(self):
        return f"[{self.left},{self.right}]"

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def copy(self) -> "Number":
        l = self.left.copy()
        r = self.right.copy()
        return Pair(left=l, right=r)

    def replace(self, src, dst):
        if self.left is src:
            self.left = dst
        elif self.right is src:
            self.right = dst
        else:
            assert False

    def leftmost(self, level=0):
        yield from self.left.leftmost(level + 1)
        yield (self, level)
        yield from self.right.leftmost(level + 1)

    def rightmost(self, level=0):
        yield from self.right.rightmost(level + 1)
        yield (self, level)
        yield from self.left.rightmost(level + 1)

    def left_neighbours(self):
        last = self
        parent = last.parent

        while parent is not None:
            if last is parent.right:
                yield from parent.left.rightmost()
            last = parent
            parent = parent.parent

    def right_neighbours(self):
        last = self
        parent = last.parent

        while parent is not None:
            if last is parent.left:
                yield from parent.right.leftmost()
            last = parent
            parent = parent.parent

    def explode(self) -> "Number":
        l = self.find_number(self.left_neighbours())
        if l is not None:
            l.value += self.left.value
        r = self.find_number(self.right_neighbours())
        if r is not None:
            r.value += self.right.value
        num = Literal(value=0, parent=self.parent)
        self.parent.replace(self, num)
        return num

    def find_number(self, gen):
        for (item, _) in gen:
            if isinstance(item, Literal):
                return item
        return None


def parse(data: str) -> Tuple[Number, str]:
    assert data

    if data[0] == "[":
        left, data = parse(data[1:])
        assert data[0] == ","
        right, data = parse(data[1:])
        assert data[0] == "]"
        return (Pair(left=left, right=right), data[1:])
    else:
        i = 0
        while i < len(data) and data[i].isnumeric():
            i += 1
        num = data[:i]
        assert num.isnumeric()
        return (Literal(value=int(num)), data[i:])


numbers = []
with open("input.txt") as f:
    for line in f:
        number, data = parse(line.strip())
        assert not data
        numbers.append(number)


max_magnitude = 0
for (i, j) in itertools.combinations(numbers, 2):
    max_magnitude = max(max_magnitude, (i.copy() + j.copy()).reduce().magnitude())
    max_magnitude = max(max_magnitude, (j.copy() + i.copy()).reduce().magnitude())
print(max_magnitude)
