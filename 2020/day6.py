import math


groups = []
group = set()
count = 0
with open("input.txt") as f:
    for row in f:
        line = row.strip()
        if not line:
            groups.append(group)
            group = set()
            count = 0
        else:
            if count == 0:
                group = set(line)
            else:
                group &= set(line)
            count += 1
    if group:
        groups.append(group)
print(sum(len(x) for x in groups))
