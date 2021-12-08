import dataclasses
import itertools
from collections import defaultdict
from typing import List


@dataclasses.dataclass
class Entry:
    signals: List[List[int]]
    output: List[List[int]]

    def __post_init__(self):
        self.signals = [tuple("abcdefg".index(v) for v in sorted(d.strip())) for d in self.signals]
        self.output = [tuple("abcdefg".index(v) for v in sorted(o.strip())) for o in self.output]


entries = []
with open("input.txt") as f:
    for line in f:
        a, b = line.strip().split(" | ")
        entries.append(Entry(signals=a.split(), output=b.split()))

connection_map = {
    0: (0, 1, 3, 4, 5, 6),
    1: (1, 4),
    2: (0, 1, 2, 5, 6),
    3: (0, 1, 2, 4, 5),
    4: (1, 2, 3, 4),
    5: (0, 2, 3, 4, 5),
    6: (0, 2, 3, 4, 5, 6),
    7: (0, 1, 4),
    8: (0, 1, 2, 3, 4, 5, 6),
    9: (0, 1, 2, 3, 4, 5)
}
length_to_digits = defaultdict(set)
for (k, v) in connection_map.items():
    length_to_digits[len(v)].add(k)


def solve(entry: Entry) -> int:
    signals_to_digit = {}
    for signal in entry.signals:
        digits = length_to_digits[len(signal)]
        if len(digits) == 1:
            signals_to_digit[signal] = list(digits)[0]

    def check(signals_to_digit):
        mapping = sorted(signals_to_digit.items(), key=lambda v: len(v))
        possible = {v: set(range(7)) for v in range(7)}
        for (signal, digit) in mapping:
            signal_set = set(signal)
            positions = connection_map[digit]
            for position in positions:
                available = possible[position]
                if signal_set.isdisjoint(available):
                    return False
                possible[position] = possible[position].intersection(signal_set)
        return True

    def assign(groups, signals_to_digit):
        if not groups:
            return signals_to_digit
        signals = groups.pop()
        digits = list(length_to_digits[len(signals[0])])
        for digit_permutation in itertools.permutations(digits):
            s = dict(signals_to_digit)
            for (digit, signal) in zip(digit_permutation, signals):
                s[signal] = digit
            if check(s):
                ret = assign(list(groups), s)
                if ret is not None:
                    return ret

    signals_to_digit = assign([
        [s for s in entry.signals if len(s) == 6],
        [s for s in entry.signals if len(s) == 5]
    ], signals_to_digit)
    assert signals_to_digit

    return int("".join([str(signals_to_digit[signal]) for signal in entry.output]))


sum = 0
for entry in entries:
    sum += solve(entry)
print(sum)
