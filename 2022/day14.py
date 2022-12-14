def normalize(value: int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


map = {}
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        points = [tuple(int(v) for v in point.split(",")) for point in line.split(" -> ")]

        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            point = start
            map[start] = "#"
            while point != end:
                dir_x = normalize(end[0] - point[0])
                dir_y = normalize(end[1] - point[1])
                point = (point[0] + dir_x, point[1] + dir_y)
                map[point] = "#"
lowest_y = max(map.keys(), key=lambda key: key[1])[1]
floor_y = lowest_y + 2


def generate_sand() -> bool:
    moves = [
        (0, 1),
        (-1, 1),
        (1, 1)
    ]

    position = (500, 0)
    while True:
        moved = False
        for move in moves:
            next_pos = (position[0] + move[0], position[1] + move[1])
            if next_pos[1] == floor_y:
                map[position] = "o"
                return False
            if next_pos not in map:
                position = next_pos
                moved = True
                break
        if not moved:
            if position == (500, 0):
                return True
            else:
                map[position] = "o"
                return False


counter = 0
while True:
    if generate_sand():
        break
    counter += 1
print(counter + 1)

# 29804 too low
