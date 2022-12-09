from typing import Tuple

commands = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        cmd, count = line.split()
        commands.append((cmd, int(count)))


def normalize(value: int) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0


def update_tail(head: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:
    head_row, head_col = head
    tail_row, tail_col = tail

    new_tail = tail

    row_dist = abs(head_row - tail_row)
    row_col = abs(head_col - tail_col)
    if row_dist > 1 or row_col > 1:
        move_row = normalize(head_row - tail_row)
        move_col = normalize(head_col - tail_col)

        new_tail = (tail[0] + move_row, tail[1] + move_col)

    # print(f"H: {head}, T: {tail}, NT: {new_tail}")
    return new_tail


def print_grid(dim: int):
    start = -dim // 2

    for row in range(dim):
        for col in range(dim):
            r = start + row
            c = start + col

            char = "."
            if (r, c) == head:
               char = "H"
            else:
                for (index, t) in enumerate(tail):
                    if (r, c) == t:
                        char = str(index + 1)
                        break
            if char == "." and (r, c) == (0, 0):
                char = "s"
            print(char, end="")
        print()
    print()


head = (0, 0)
tail = [(0, 0) for _ in range(9)]
positions = {(0, 0)}

dirs = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0)
}

dim = 26
print_grid(dim)

for command, count in commands:
    dir = dirs[command]
    for _ in range(count):
        head = (head[0] + dir[0], head[1] + dir[1])
        prev = head
        new_tail = []
        for item in tail:
            new_item = update_tail(prev, item)
            new_tail.append(new_item)
            prev = new_item
        tail = new_tail
        positions.add(tail[-1])
        # print_grid(dim)
    # print(head, tail)

print(len(positions))

# 2454 too low
