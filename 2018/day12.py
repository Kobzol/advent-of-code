with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

state = "#.#.#...#..##..###.##.#...#.##.#....#..#.#....##.#.##...###.#...#######.....##.###.####.#....#.#..##"
arcs = {}

for line in lines:
    line = line.split(" => ")
    arcs[line[0]] = line[1]

index = 0
for gen in range(1, 5000):
    state = "....." + state + "....."
    next = list(state)
    index += 5

    for i in range(2, len(state) - 3):
        for arc in arcs:
            if arc == state[i-2:i+3]:
                next[i] = arcs[arc]
    state = "".join(next)

    if (gen % 1) == 0:
        s = 0
        for i, c in enumerate(state):
            if c == "#":
                s += i - index
        print(gen, state.find("#") - index, state.rfind("#") - index, s)

s = 0
for i, c in enumerate(state):
    if c == "#":
        s += i - index
print(s)
