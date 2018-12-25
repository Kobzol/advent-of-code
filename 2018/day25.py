with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

points = []
clusters = []
for line in lines:
    point = tuple(map(int, line.split(",")))
    points.append(point)
    clusters.append([point])


def dist(a, b):
    return sum(abs(x-y) for (x, y) in zip(a, b))


while True:
    change = False
    for (i, c) in enumerate(clusters):
        for c2 in clusters[i+1:]:
            for a in c[:]:
                for b in c2[:]:
                    if dist(a, b) <= 3:
                        c.append(b)
                        c2.remove(b)
                        change = True
            if len(c2) == 0:
                clusters.remove(c2)
    print(len(clusters))
    if not change:
        break
