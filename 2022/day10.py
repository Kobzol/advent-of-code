import collections
import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class Instruction:
    command: List[str]
    remaining_cycles: int


commands = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        commands.append(line.split())


def execute(instruction: Instruction, x: int) -> int:
    if instruction.command[0] == "addx":
        return x + int(instruction.command[1])
    return x


def load_instruction() -> Instruction:
    inst = commands.popleft()
    lengths = {
        "noop": 1,
        "addx": 2
    }
    return Instruction(command=inst, remaining_cycles=lengths[inst[0]])


commands = collections.deque(commands)

x = 1
current: Optional[Instruction] = load_instruction()
pixels = [["."] * 40 for _ in range(6)]

for cycle in range(240):
    if current.remaining_cycles == 0:
        x = execute(current, x)
        current = load_instruction()

    current.remaining_cycles -= 1

    norm_cycle = cycle % 40
    row = cycle // 40
    if norm_cycle - 1 <= x <= norm_cycle + 1:
        pixels[row][norm_cycle] = "#"

for row in range(6):
    for col in range(40):
        print(pixels[row][col], end="")
    print()
