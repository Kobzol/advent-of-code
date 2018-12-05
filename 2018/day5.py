with open("input.txt", "r") as f:
    data = f.read().strip()


counts = {}

for index in range(0, len(data) - 1):
    counts[data[index].lower()] = 1

input = data
min = 10e10
for c in counts:
    data = input.replace(c.lower(), "").replace(c.upper(), "")
    i = 0
    while True:
        found = False
        for index in range(i, len(data) - 1):
            i += 1
            if data[index].lower() == data[index + 1].lower() and data[index] != data[index + 1]:
                data = data[:index] + data[index + 2:]
                found = True
                i = max(0, i - 3)
                break
        if not found:
            break
    if len(data) < min:
        min = len(data)
    print(c)

print(min)
