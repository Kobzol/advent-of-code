import itertools

grid = []

with open("input.txt") as f:
    for line in f:
        grid.append(list(line.strip()))


def hash(state):
    return tuple(itertools.chain.from_iterable(state))


def is_valid(state, row, col):
    return 0 <= row < 5 and 0 <= col < 5


def count_neighbours(state, x, y):
    neighbours = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    )
    count = 0
    for i, j in neighbours:
        tx = x + i
        ty = y + j
        if is_valid(state, tx, ty) and state[tx][ty] == '#':
            count += 1
    return count


def move(state):
    next_state = [list(r) for r in state]
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            neighbours = count_neighbours(state, i, j)
            next = col
            if col == '#' and neighbours != 1:
                next = '.'
            elif col == '.' and neighbours in (1, 2):
                next = '#'
            next_state[i][j] = next
    return next_state


def score(state):
    p = 0
    s = 0
    for row in state:
        for col in row:
            if col == '#':
                s += pow(2, p)
            p += 1
    return s


def get_neighbours(state, level, i, j):
    assert (i, j) != (2, 2)
    neighbours = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    )
    inner = {
        (1, 2): ((0, 0), (0, 1)),
        (2, 1): ((0, 0), (1, 0)),
        (2, 3): ((0, 4), (1, 0)),
        (3, 2): ((4, 0), (0, 1))
    }

    def norm(row, col):
        if row == -1:
            return (1, 2)
        elif row == 5:
            return (3, 2)
        elif col == -1:
            return (2, 1)
        elif col == 5:
            return (2, 3)
        else:
            assert False

    for (x, y) in neighbours:
        tx = x + i
        ty = y + j
        if is_valid(state, tx, ty):
            if (tx, ty) == (2, 2):
                start, dir = inner[(i, j)]
                for _ in range(5):
                    yield (level + 1, *start)
                    start = (start[0] + dir[0], start[1] + dir[1])
            else:
                yield (level, tx, ty)
        else:
            yield (level - 1, *norm(tx, ty))


def move_sparse(state):
    next_state = set()
    for level, i, j in state:
        neighbours = tuple(get_neighbours(state, level, i, j))
        bugs = sum(1 if n in state else 0 for n in neighbours)
        if bugs == 1:
            next_state.add((level, i, j))

        for l, x, y in neighbours:
            if (l, x, y) in state:
                continue
            target_neighbours = tuple(get_neighbours(state, l, x, y))
            bugs = sum(1 if n in state else 0 for n in target_neighbours)
            if bugs in (1, 2):
                next_state.add((l, x, y))

    return next_state


state = set()
for i, row in enumerate(grid):
    for j, col in enumerate(row):
        if col == '#':
            state.add((0, i, j))


for i in range(200):
    state = move_sparse(state)

print(len(state))
