import math


def rotate_point(p, angle):
    angle = math.radians(angle)

    s = math.sin(angle)
    c = math.cos(angle)

    xnew = p[0] * c - p[1] * s
    ynew = p[0] * s + p[1] * c

    return [int(round(xnew)), int(round(ynew))]


pos = [0, 0]
waypoint = [10, 1]

with open("input.txt") as f:
    for row in f:
        row = row.strip()
        dir = row[0]
        count = int(row[1:])
        print(dir, count)
        if dir == "N":
            waypoint[1] += count
        elif dir == "S":
            waypoint[1] -= count
        elif dir == "E":
            waypoint[0] += count
        elif dir == "W":
            waypoint[0] -= count
        elif dir == "F":
            pos[0] += waypoint[0] * count
            pos[1] += waypoint[1] * count
        elif dir == "L":
            waypoint = rotate_point(waypoint, count)
        elif dir == "R":
            waypoint = rotate_point(waypoint, -count)
        print(pos, waypoint)

print(pos)
print(int(sum(abs(x) for x in pos)))
