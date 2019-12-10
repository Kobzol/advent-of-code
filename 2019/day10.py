import math

map = []

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        map.append([x for x in line])

asteroids = set()
for row, line in enumerate(map):
    for col, c in enumerate(line):
        if c == "#":
            asteroids.add((row, col))


def lies_on(line, start, point):
    dir = vec_create(start, point)
    return vec_cmp(vec_normalize(line), vec_normalize(dir)) and vec_length(dir) >= vec_length(line)


def vec_cmp(a, b):
    def cmp(x, y):
        return abs(x - y) < 0.0001

    return cmp(a[0], b[0]) and cmp(a[1], b[1])


def sign(x):
    return 1 if x >= 0 else 0


def vec_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def vec_normalize(v):
    l = vec_length(v)
    return tuple(x / l for x in v)


def vec_create(a, b):
    return (b[0] - a[0], b[1] - a[1])


def get_line(a, b):
    return vec_create(a, b)


def rad_to_deg(v):
    return v * (180.0 / math.pi)


def get_visible(asteroid, asteroids):
    blocked = {asteroid}
    candidates = sorted(asteroids)
    for candidate in candidates:
        if candidate in blocked:
            continue
        line = get_line(asteroid, candidate)
        for other in candidates:
            if other not in (asteroid, candidate) and lies_on(line, asteroid, other):
                blocked.add(other)
    return set(asteroids) - blocked


def print_map(m):
    for row in m:
        for col in row:
            print(col, end='')
        print()
    print()


pos = (29, 28)
# pos = (3, 8)
# pos = (13, 11)


def blast(asteroids, pos):
    vaporized = 0
    current_angle = 0
    blasted = set()

    while True:
        def calc_angle(v):
            vec = vec_create(pos, v)
            angle = (rad_to_deg(math.atan2(vec[1], -vec[0])) + 360) % 360
            return ((angle - current_angle) + 360) % 360

        def next_iteration():
            nonlocal current_angle, asteroids, blasted
            current_angle = 0
            asteroids -= blasted
            blasted = set()

        while True:
            visible = get_visible(pos, asteroids)
            if not visible:
                return
            nearest = sorted(tuple((v, calc_angle(v)) for v in visible if v not in blasted),
                             key=lambda v: v[1])
            if not nearest:
                next_iteration()
            else:
                break
        target, angle = nearest[0]

        current_angle = current_angle + angle
        blasted.add(target)

        print(vaporized, target)
        # map[target[0]][target[1]] = str(vaporized % 9 + 1)
        # print_map(map)
        vaporized += 1
        if vaporized > 210:
            break


blast(asteroids, pos)
