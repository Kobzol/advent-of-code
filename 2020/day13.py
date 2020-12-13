with open("input.txt") as f:
    buses_str = [x for x in f.readline().strip().split(",")]

buses = []
for (index, bus) in enumerate(buses_str):
    if bus != "x":
        bus = int(bus)
        buses.append((bus, (bus - index) % bus))

buses = sorted(buses, key=lambda x: -x[0])


def closest_divisable(number, divident):
    return number + (divident - number % divident) % divident


def closest_divisable_rem(number, divident, add, rem):
    while number % divident != rem:
        number += add
    return number


def check(n, buses):
    n = closest_divisable_rem(n, buses[1][0], buses[0][0], buses[1][1])
    assert n % buses[0][0] == buses[0][1]
    assert n % buses[1][0] == buses[1][1]

    for (bus, index) in buses[2:]:
        if n % bus != index:
            return n
    print(n)
    exit()


# index = closest_divisable_rem(100000000000000, buses[0][0], 1, buses[0][1])
# while True:
#     index = check(index, buses)
#     index += buses[0][0]


def check2(base, multiplier, divident, rem):
    while True:
        if base % divident == rem:
            return base
        base += multiplier


number = closest_divisable_rem(100000000000000, buses[0][0], 1, buses[0][1])
bus_index = 1
multiplier = buses[0][0]
while bus_index < len(buses):
    number = check2(number, multiplier, buses[bus_index][0], buses[bus_index][1])
    multiplier *= buses[bus_index][0]
    bus_index += 1
print(number)
