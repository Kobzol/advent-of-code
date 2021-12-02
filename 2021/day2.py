import dataclasses


@dataclasses.dataclass(frozen=True)
class Command:
    pass


@dataclasses.dataclass(frozen=True)
class Down(Command):
    amount: int


@dataclasses.dataclass(frozen=True)
class Up(Command):
    amount: int


@dataclasses.dataclass(frozen=True)
class Right(Command):
    amount: int


def parse(command: str) -> Command:
    cmd, arg = command.split()
    arg = int(arg)
    if cmd == "down":
        return Down(amount=arg)
    elif cmd == "up":
        return Up(amount=arg)
    elif cmd == "forward":
        return Right(amount=arg)
    else:
        assert False


@dataclasses.dataclass(frozen=True)
class State:
    x: int = 0
    depth: int = 0
    aim: int = 0


def execute(state: State, command: Command) -> State:
    if isinstance(command, Down):
        return dataclasses.replace(state, aim=state.aim + command.amount)
    elif isinstance(command, Up):
        return dataclasses.replace(state, aim=state.aim - command.amount)
    elif isinstance(command, Right):
        return dataclasses.replace(state, x=state.x + command.amount,
                                   depth=state.depth + state.aim * command.amount)
    else:
        assert False


state = State()

with open("input.txt") as f:
    for row in f:
        cmd = parse(row.strip())
        state = execute(state, cmd)

print(state.x * state.depth)
