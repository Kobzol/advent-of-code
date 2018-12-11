import numpy as np

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

integral = np.zeros((300, 300))
values = np.zeros((300, 300))

gridid = 3214

maximum = 0
target = None
for y in range(300):
    for x in range(300):
        val = 0
        if y == 0:
            val += integral[0, max(0, x - 1)]
        elif x == 0:
            val += integral[max(0, y - 1), 0]
        else:
            val -= integral[y - 1, x - 1]
            val += integral[y - 1, x]
            val += integral[y, x - 1]

        rack = x + 10
        pl = rack * y
        pl += gridid
        pl *= rack
        pl = (pl // 100) % 10
        pl -= 5
        val += pl
        integral[y, x] = val
        values[y, x] = pl


def sumrect(i, j, width):
    if width == 1:
        return values[i, j]

    width -= 1
    bi = i + width
    rj = j + width

    if bi >= 300 or rj >= 300:
        return -1

    val = integral[bi, rj]
    if i > 0 and j > 0:
        val += integral[i - 1, j - 1]
    if i > 0:
        val -= integral[i - 1, rj]
    if j > 0:
        val -= integral[bi, j - 1]

    return val


maximum = 0
for y in range(300):
    for x in range(300):
        maxwidth = min(300 - x, 300 - y)
        for width in range(1, maxwidth + 1):
            value = sumrect(y, x, width)
            if value > maximum:
                maximum = value
                target = (x, y, width)
print(maximum, target)
