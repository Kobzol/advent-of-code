ranges = []

with open("input.txt") as f:
    for row in f:
        row = row.strip()
        a, b = row.split(",")
        r0a, r0b = [int(v) for v in a.split("-")]
        r1a, r1b = [int(v) for v in b.split("-")]
        ranges.append(((r0a, r0b), (r1a, r1b)))


count = 0
for ((a, b), (c, d)) in ranges:
    # if a > c:
    #     (c, d, a, b) = (a, b, c, d)

    x = set(range(a, b + 1))
    y = set(range(c, d + 1))
    if len(x.intersection(y)) > 0:
        count += 1
print(count)
