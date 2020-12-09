import itertools
import collections

LENGTH = 25


def find_sum(code, number):
    for (a, b) in itertools.combinations(code, 2):
        if a + b == number:
            assert a != b
            return True
    return False


code = collections.deque(maxlen=LENGTH)
target = None
with open("input.txt") as f:
    for row in f:
        number = int(row.strip())
        if len(code) == LENGTH:
            if not find_sum(code, number):
                target = number
                break
        code.append(number)

numbers = []
with open("input.txt") as f:
    for row in f:
        numbers.append(int(row.strip()))

for length in range(2, len(numbers) + 1):
    for i in range(0, len(numbers)):
        items = numbers[i:i+length]
        if sum(items) == target:
            print(min(items) + max(items))
