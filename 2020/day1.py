items = []

with open("input.txt") as f:
    for row in f:
        line = row.strip()
        items.append(int(line))

for i, item1 in enumerate(items):
    for j, item2 in enumerate(items):
        for k, item3 in enumerate(items):
            if i == j or j == k or i == k:
                continue
            if item1 + item2 + item3 == 2020:
                print(item1 * item2 * item3)
