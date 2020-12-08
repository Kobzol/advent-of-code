class CPU:
    def __init__(self, program):
        self.accumulator = 0
        self.pc = 0
        self.program = tuple(program)

    def execute(self):
        if self.pc == len(self.program):
            print(self.accumulator)
            return True

        opcode, *args = self.program[self.pc]
        if opcode == "acc":
            self.accumulator += int(args[0])
            self.pc += 1
        elif opcode == "nop":
            self.pc += 1
        elif opcode == "jmp":
            self.pc += int(args[0])
        else:
            assert False
        return False


def run(cpu, max_steps=10000):
    for _ in range(max_steps):
        if cpu.execute():
            break


program = []
with open("input.txt") as f:
    for row in f:
        line = row.strip()
        instruction = tuple(line.split())
        program.append(instruction)

for (index, inst) in enumerate(program):
    copy = list(program)
    opcode = inst[0]
    if opcode == "nop":
        copy[index] = ("jmp", *copy[index][1:])
    elif opcode == "jmp":
        copy[index] = ("nop", *copy[index][1:])
    cpu = CPU(copy)
    run(cpu)
