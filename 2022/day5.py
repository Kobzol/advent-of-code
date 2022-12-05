import dataclasses


@dataclasses.dataclass
class Command:
    origin: int
    dest: int
    count: int


input = []
count = None
commands = []

with open("input.txt") as f:
    for row in f:
        if not row.strip():
            break

        if row.strip().startswith("1"):
            count = int(row.strip().split()[-1])
        else:
            input.append(row.rstrip("\n"))
    for row in f:
        items = row.strip().split()
        command = Command(
            count=int(items[1]),
            origin=int(items[3]),
            dest=int(items[5]),
        )
        commands.append(command)

stacks = [[] for _ in range(count)]
for row in input:
    if len(row) < 4 * count:
        row = row + " " * (4 * count - len(row))
    print(row, len(row))
    for index in range(count):
        target = 1 + index * 4
        if row[target] != " ":
            stacks[index].insert(0, row[target])


def move(command: Command):
    # print(f"Move from {origin} to {destionation}")
    origin = stacks[command.origin - 1]
    items = origin[-command.count:]
    stacks[command.origin - 1] = origin[:-command.count]
    stacks[command.dest - 1].extend(items)



def print_crates():
    height = max(len(s) for s in stacks)
    for row in range(height - 1, -1, -1):
        for col in range(count):
            if row < len(stacks[col]):
                print(stacks[col][row], end="")
            else:
                print(" ", end="")
        print()
    print()

print_crates()
for command in commands:
    move(command)
    # print_crates()


print("".join(s[-1] for s in stacks))
