import math


def find_position(input, range, low):
    start, end = range
    for c in input:
        if c == low:
            half = start + math.floor((end - start) / 2)
            end = half
        else:
            half = start + math.ceil((end - start) / 2)
            start = half
    assert start == end
    return start


def position(boarding_pass):
    row = find_position(boarding_pass[:7], (0, 127), "F")
    col = find_position(boarding_pass[7:], (0, 7), "L")
    return row * 8 + col


items = []
with open("input.txt") as f:
    for row in f:
        line = row.strip()
        items.append(position(line))

print(sorted(items))
seats = set(items)
print(set(range(max(seats) + 1)) - seats)
