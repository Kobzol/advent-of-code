import traceback

import pygame


class Program:
    def __init__(self, memory, input):
        self.memory = {}
        for i, item in enumerate(memory):
            self.memory[i] = item
        self.input = list(input[::-1])
        self.output = None
        self.pc = 0
        self.relbase = 0

    def add_input(self, c):
        self.input = [c] + self.input

    def read(self):
        return self.input.pop()

    def write(self, c):
        self.output = c

    def memread(self, address):
        if isinstance(address, Arg):
            address = address.address_eval()
        assert address >= 0
        if address not in self.memory:
            self.memory[address] = 0
        return self.memory[address]

    def memwrite(self, address, value):
        if isinstance(address, Arg):
            address = address.address_eval()
        self.memory[address] = value


class Arg:
    def __init__(self, val, mode, program):
        self.val = val
        self.mode = mode
        self.program = program

    def eval(self):
        if self.mode == 0:
            return self.program.memread(self.val)
        elif self.mode == 1:
            return self.val
        elif self.mode == 2:
            return self.program.memread(self.val + self.program.relbase)
        else:
            assert False

    def address_eval(self):
        assert self.mode != 1
        if self.mode == 2:
            return self.val + self.program.relbase
        return self.val


def stop(program, args):
    return True


def add(program, args):
    program.memwrite(args[2], args[0].eval() + args[1].eval())


def mul(program, args):
    program.memwrite(args[2], args[0].eval() * args[1].eval())


def read(program, args):
    program.memwrite(args[0], program.read())


def write(program, args):
    program.write(args[0].eval())


def jumpiftrue(program, args):
    if args[0].eval() != 0:
        return args[1].eval()


def jumpiffalse(program, args):
    if args[0].eval() == 0:
        return args[1].eval()


def lessthan(program, args):
    val = 0
    if args[0].eval() < args[1].eval():
        val = 1
    program.memwrite(args[2], val)


def equals(program, args):
    val = 0
    if args[0].eval() == args[1].eval():
        val = 1
    program.memwrite(args[2], val)


def modify_relbase(program, args):
    program.relbase += args[0].eval()


instructions = {
    99: (0, stop),
    1: (3, add),
    2: (3, mul),
    3: (1, read),
    4: (1, write),
    5: (2, jumpiftrue),
    6: (2, jumpiffalse),
    7: (3, lessthan),
    8: (3, equals),
    9: (1, modify_relbase)
}


def run_inst(program):
    try:
        opcode = program.memread(program.pc) % 100
        (param_count, fn) = instructions[opcode]
        modes = list(int(c) for c in str(program.memread(program.pc) // 100)[::-1])
        modes += [0] * (param_count - len(modes))
        args = tuple(Arg(v, m, program) for (v, m) in
                     zip((program.memread(a) for a in
                          range(program.pc + 1, program.pc + 1 + param_count)), modes))
        ret = fn(program, args)
        if ret is True:
            return True
        elif isinstance(ret, int):
            program.pc = ret
        else:
            program.pc += 1 + param_count
    except:
        traceback.print_exc()
    return False


def turn(dir, new_dir):
    if new_dir == 0:
        return (-dir[1], dir[0])
    elif new_dir == 1:
        return (dir[1], -dir[0])
    else:
        assert False


with open("input.txt") as f:
    memory = list(int(v) for v in f.read().strip().split(","))


memory[0] = 2
program = Program(memory, ())


screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
tile_size = 15
game_map = {}
paddle = (0, 0)
ball = (0, 0)
color_map = {
    0: (0, 0, 0),           # empty
    1: (0, 255, 0),         # wall
    2: (255, 0, 0),         # block
    3: (255, 255, 255),     # paddle
    4: (0, 0, 255),         # ball
}
score = 0
input = 0
steps_per_iter = 1


def simulate(program, input):
    global ball, paddle, score

    output = []
    while len(output) < 3:
        program.output = None
        program.input = [input]
        end = run_inst(program)
        if end:
            return True
        if program.output is not None:
            output.append(program.output)

    x, y, tile = output
    if x == -1 and y == 0:
        score = tile
        print("Score: {}".format(score))
    else:
        game_map[(x, y)] = tile

    if tile == 3:
        paddle = (x, y)
    elif tile == 4:
        ball = (x, y)

    return False


for i in range(968):
    simulate(program, 0)


keys = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False
}

while True:
    delta = clock.tick(1000) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in keys:
                keys[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in keys:
                keys[event.key] = False

    input = 0
    if ball[0] > paddle[0]:
        input = 1
    elif ball[0] < paddle[0]:
        input = -1

    for i in range(steps_per_iter):
        if simulate(program, input):
            break

    screen.blit(background, (0, 0))
    for ((x, y), item) in game_map.items():
        x = x * tile_size
        y = y * tile_size
        color = color_map[item]
        pygame.draw.rect(screen, color, ((x, y), (tile_size, tile_size)))

    pygame.display.flip()

# 18642 too high
