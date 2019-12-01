import math


def calculate_fuel(mass):
    return max(0, math.floor(mass / 3) - 2)


total = 0
with open("input.txt") as f:
    for l in f:
        counter = 0
        input = float(l.strip())
        while True:
            fuel = calculate_fuel(input)
            if fuel == 0:
                break
            counter += fuel
            input = fuel
        total += counter

print(total)
