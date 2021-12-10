import dataclasses
from typing import List, Union

import numpy as np

lines = []
with open("input.txt") as f:
    for line in f:
        lines.append(line.strip())

start = "([{<"
end = ")]}>"
scores = (3, 57, 1197, 25137)


@dataclasses.dataclass(frozen=True)
class OK:
    pass


@dataclasses.dataclass(frozen=True)
class Corrupted:
    score: int


@dataclasses.dataclass
class Incomplete:
    stack: List[str]


Result = Union[OK, Corrupted, Incomplete]


def parse(line: str) -> Result:
    stack = []
    for char in line:
        if char in start:
            stack.append(char)
        elif char in end:
            index = end.index(char)
            expected_index = start.index(stack.pop())
            if index != expected_index:
                return Corrupted(score=scores[index])
        else:
            assert False
    if not stack:
        return OK()
    return Incomplete(stack=stack)


complete_scores = []
for line in lines:
    result = parse(line)
    s = 0
    if isinstance(result, Incomplete):
        for c in result.stack[::-1]:
            s *= 5
            s += start.index(c) + 1
        complete_scores.append(s)

print(int(np.median(complete_scores)))
