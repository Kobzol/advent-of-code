import numpy as np

points = []
velocities = []

with open("input.txt", "r") as f:
    for line in f.readlines():
        line = line[10:]
        x = int(line[:line.index(",")])
        line = line[line.index(",") + 1:]
        y = int(line[:line.index(">")])
        line = line[line.index(">") + 12:]
        vx = int(line[:line.index(",")])
        line = line[line.index(",") + 1:]
        vy = int(line[:line.index(">")])
        points.append([x, y])
        velocities.append((vx, vy))

index = 0
with open("out.txt", "w") as f:
    while True:
        xmin = min([p[0] for p in points])
        ymin = min([p[1] for p in points])
        xmax = max([p[0] for p in points])
        ymax = max([p[1] for p in points])

        if abs(xmax - xmin) < 100:
            print("close", index)
            data = np.zeros((xmax-xmin + 1, ymax-ymin + 1), dtype=np.int8)
            for p in points:
                data[p[0] - xmin, p[1] - ymin] = 1

            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    f.write('x' if data[i, j] else ' ')
                f.write('\n')
            f.write("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX{}\n".format(index))
            f.flush()

        for i, p in enumerate(points):
            p[0] += velocities[i][0]
            p[1] += velocities[i][1]
        index += 1
