grid = []
width = 0
height = 0

with open("input.txt") as f:
    for row in f:
        grid.extend(row.strip())
        width = len(row)
        height += 1


def get(row, col):
    return row * width + col


def is_valid(row, col):
    return 0 <= row < height and 0 <= col < width


DIRECTIONS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
    (-1, -1)
]


def move(grid):
    newgrid = list(grid)
    change = False
    for row in range(height):
        for col in range(width):
            item = grid[get(row, col)]
            if item != ".":
                alive = 0
                for (row_dir, col_dir) in DIRECTIONS:
                    r = row + row_dir
                    c = col + col_dir
                    while is_valid(r, c):
                        value = grid[get(r, c)]
                        if value == "L":
                            break
                        elif value == "#":
                            alive += 1
                            break
                        r += row_dir
                        c += col_dir
                if item == "L" and alive == 0:
                    newgrid[get(row, col)] = "#"
                    change = True
                elif item == "#" and alive >= 5:
                    newgrid[get(row, col)] = "L"
                    change = True
    return newgrid, change


while True:
    new, changed = move(grid)
    if not changed:
        break
    grid = new

print(len(tuple(c for c in grid if c == "#")))
