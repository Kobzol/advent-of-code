import collections

rules = {}
with open("input.txt") as f:
    start = f.readline().strip()
    f.readline()

    for line in f:
        key, val = line.strip().split(" -> ")
        assert key not in rules
        rules[key] = val

"""
def step(item: str) -> str:
    result = ""
    for index in range(len(item) - 1):
        key = item[index:index + 2]
        result += item[index]
        if key in rules:
            result += rules[key]
    result += item[-1]

    return result


def solve_item(item: Tuple[str, int], stack: List[Tuple[str, int]], counts: Dict[str, int]):
    item, steps = item
    for i in range(steps):
        key = item + stack[-1][0]
        if key in rules:
            stack.append((rules[key], (steps - i) - 1))
        else:
            break
    counts[item] += 1


def solve(item: str, steps: int) -> Dict[str, int]:
    counts = collections.Counter()
    stack = [(c, steps) for c in item[::-1]]
    iter = 0
    while len(stack) > 1:
        item = stack.pop()
        solve_item(item, stack, counts)
        iter += 1
        if iter % 100000 == 0:
            print(iter, len(stack))
    counts[stack.pop()[0]] += 1
    return counts
"""

# for i in tqdm.tqdm(range(40)):
#     start = step(start)
#
# counter = collections.Counter()
# for item in start:
#     counter[item] += 1
# values = list(counter.values())
pairs = collections.Counter()
chars = collections.Counter()
for index in range(len(start) - 1):
    key = start[index:index + 2]
    pairs[key] += 1
for char in start:
    chars[char] += 1

for i in range(40):
    next_pairs = collections.Counter()
    for (pair, count) in pairs.items():
        if pair in rules:
            char = rules[pair]
            p1 = pair[0] + char
            p2 = char + pair[1]
            chars[char] += count
            next_pairs[p1] += count
            next_pairs[p2] += count
        else:
            next_pairs[pair] += count
    pairs = next_pairs

values = chars.values()
print(max(values) - min(values))
