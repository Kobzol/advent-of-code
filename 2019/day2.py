def evaluate(memory, pc=0):
    while True:
        opcode = memory[pc]
        if opcode == 99:
            break
        else:
            op1 = memory[memory[pc + 1]]
            op2 = memory[memory[pc + 2]]
            target = memory[pc + 3]
            if opcode == 1:
                memory[target] = op1 + op2
            elif opcode == 2:
                memory[target] = op1 * op2
        pc += 4
    return memory[0]


with open("input.txt") as f:
    instructions = [int(v) for v in f.read().split(",")]

for noun in range(0, 100):
    for verb in range(0, 100):
        memory = list(instructions)
        memory[1] = noun
        memory[2] = verb
        if evaluate(memory) == 19690720:
            print(noun, verb, 100 * noun + verb)
