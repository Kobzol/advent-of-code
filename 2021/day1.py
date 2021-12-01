items = []

with open("input.txt") as f:
    for row in f:
        line = int(row.strip())
        items.append(line)

last = None
more = 0
for i in range(len(items)):
    slice = items[i:i+3]
    if len(slice) == 3 and last is not None and sum(slice) > last:
        more += 1
    last = sum(slice)
print(more)
