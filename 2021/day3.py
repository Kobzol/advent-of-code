from collections import Counter
from typing import List, Union

numbers = []
with open("input.txt") as f:
    for line in f:
        numbers.append(line.strip())


gamma = ""
epsilon = ""


def most_common(nums: List[str], position: int) -> Union[int, bool]:
    counts = Counter()
    for num in nums:
        counts[num[position]] += 1
    if counts["0"] > counts["1"]:
        return 0
    elif counts["1"] > counts["0"]:
        return 1
    else:
        return True


def invert(v: int) -> int:
    if v is True:
        return True
    return 1 - v


def from_bin(digits: str) -> int:
    return int(digits, 2)


nums = list(numbers)
position = 0
while len(nums) > 1:
    r = most_common(nums, position)
    if r is True:
        nums = [n for n in nums if n[position] == "1"]
    else:
        nums = [n for n in nums if n[position] == str(r)]
    position += 1
oxygen = from_bin(nums[0])


nums = list(numbers)
position = 0
while len(nums) > 1:
    r = most_common(nums, position)
    if r is True:
        nums = [n for n in nums if n[position] == "0"]
    else:
        nums = [n for n in nums if n[position] == str(invert(r))]
    position += 1
scrubber = from_bin(nums[0])

print(oxygen * scrubber)
