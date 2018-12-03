with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

ids = {}

data = [0 for _ in range(1000 * 1000)]
for line in lines:
    d = line.split()
    id = int(d[0][1:])
    pos = [int(x) for x in d[2].rstrip(":").split(",")]
    dim = [int(x) for x in d[3].split("x")]

    ids[id] = []
    removed = False
    for x in range(dim[1]):
        for y in range(dim[0]):
            a = x + pos[1]
            b = y + pos[0]
            data[a * 1000 + b] += 1
            ids[id].append(a * 1000 + b)

for id in ids:
    ok = True
    for index in ids[id]:
        if data[index] != 1:
            ok = False
            break
    if ok:
        print(id)
