import dataclasses
import math
from typing import Optional, Tuple

bits = ""
with open("input.txt") as f:
    hex = f.readline().strip()
    for c in hex:
        bits += f"{int(c, 16):b}".zfill(4)


def to_num(bits: str) -> int:
    return int(bits, 2)


@dataclasses.dataclass
class Input:
    data: str

    def read_int(self, count: int) -> Tuple["Input", int]:
        num = to_num(self.data[:count])
        return (Input(data=self.data[count:]), num)

    def read_bits(self, count: int) -> Tuple["Input", str]:
        data = self.data[:count]
        return (Input(data=self.data[count:]), data)

    def __len__(self) -> int:
        return len(self.data)


@dataclasses.dataclass
class Packet:
    version: int
    type_id: int
    value: Optional[int] = int


def parse_literal_value(input: Input) -> Tuple[Input, int]:
    bits = ""
    while True:
        input, marker = input.read_int(1)
        input, value = input.read_bits(4)
        bits += value

        if marker == 0:
            break
    return (input, to_num(bits))


def parse(input: Input) -> Input:
    if not input.data:
        return
    input, version = input.read_int(3)
    input, type_id = input.read_int(3)
    if type_id == 4:
        input, literal = parse_literal_value(input)
        yield Packet(version=version, type_id=type_id, value=literal)
    else:
        input, length_type_id = input.read_int(1)

        def get_subpackets():
            nonlocal input

            if length_type_id == 0:
                input, bit_count = input.read_int(15)
                current = len(input)
                target = current - bit_count
                while len(input) > target:
                    input = yield from parse(input)
            else:
                input, packet_count = input.read_int(11)
                for _ in range(packet_count):
                    input = yield from parse(input)
        gen = (p.value for p in get_subpackets())
        if type_id == 0:
            value = sum(gen)
        elif type_id == 1:
            value = math.prod(gen)
        elif type_id == 2:
            value = min(gen)
        elif type_id == 3:
            value = max(gen)
        elif type_id == 5:
            packets = list(gen)
            assert len(packets) == 2
            value = 1 if packets[0] > packets[1] else 0
        elif type_id == 6:
            packets = list(gen)
            assert len(packets) == 2
            value = 1 if packets[0] < packets[1] else 0
        elif type_id == 7:
            packets = list(gen)
            assert len(packets) == 2
            value = 1 if packets[0] == packets[1] else 0

        yield Packet(version=version, type_id=type_id, value=value)
    return input


input = Input(data=bits)
packets = list(parse(input))
assert len(packets) == 1
print(packets[0].value)
