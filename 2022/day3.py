def char_score(item: str):
    norm = item.lower()
    value = ord(norm) - ord('a')
    bonus = 26 if item.isupper() else 0
    return value + bonus + 1


def backpack_score(backpack: str):
    assert len(backpack) % 2 == 0
    left = backpack[:len(backpack) // 2]
    right = backpack[len(backpack) // 2:]
    shared = list(set(left) & set(right))
    assert len(shared) == 1
    shared = shared[0]
    # print(shared, char_score(shared))
    return char_score(shared)


backpacks = []

with open("input.txt") as f:
    for row in f:
        row = row.strip()
        backpacks.append(row)


sum = 0
for index in range(0, len(backpacks), 3):
    group = backpacks[index:index+3]
    shared = set(group[0]) & set(group[1]) & set(group[2])
    assert len(shared) == 1
    shared = list(shared)[0]
    sum += char_score(shared)
print(sum)
