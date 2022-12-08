grid = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        grid.append([int(v) for v in line])

rows = len(grid)
cols = len(grid[0])


def left(row: int, col: int):
    col -= 1
    while col >= 0:
        yield grid[row][col]
        col -= 1


def right(row: int, col: int):
    col += 1
    while col < cols:
        yield grid[row][col]
        col += 1


def up(row: int, col: int):
    row -= 1
    while row >= 0:
        yield grid[row][col]
        row -= 1


def down(row: int, col: int):
    row += 1
    while row < rows:
        yield grid[row][col]
        row += 1


def view_distance(iter, height: int) -> int:
    count = 0
    for item in iter:
        count += 1
        if item >= height:
            break
    return count

def scenic_score(row: int, col: int) -> int:
    height = grid[row][col]
    l = view_distance(left(row, col), height)
    r = view_distance(right(row, col), height)
    d = view_distance(down(row, col), height)
    u = view_distance(up(row, col), height)

    return l * r * d * u


max_score = 0
for row in range(rows):
    for col in range(cols):
        score = scenic_score(row, col)
        # print((row, col), score)
        if score > max_score:
            max_score = score
print(max_score)
