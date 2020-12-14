def compute(value, mask):
    value = list(f"{value:036b}")

    for i in range(36):
        bit = mask[i]
        if bit in ("X", "1"):
            value[i] = bit
    return "".join(value)


def iterate_values(bitfield):
    for i in range(len(bitfield)):
        if bitfield[i] == "X":
            yield from iterate_values(bitfield[0:i] + "0" + bitfield[i + 1:])
            yield from iterate_values(bitfield[0:i] + "1" + bitfield[i + 1:])
            return
    yield int(bitfield, 2)


mask = ""
memory = {}

with open("input.txt") as f:
    for row in f:
        row = row.strip()
        start, _, value = row.split()
        if start == "mask":
            mask = value
        else:
            value = int(value)
            address_val = int(start[4:-1])
            address_val = compute(address_val, mask)
            for address in iterate_values(address_val):
                memory[address] = value

print(sum(memory.values()))
