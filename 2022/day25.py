import math


def to_snafu(value: int) -> str:
    digits = []
    digit_count = round(math.log(value, 5))
    current_value = 0
    for i in range(digit_count, -1, -1):
        multiplier = math.pow(5, i)
        target = value - current_value
        target_abs = abs(target)
        digit = round(target_abs / multiplier)
        if target > 0:
            assert digit in (0, 1, 2)
            current_value += digit * multiplier
        else:
            current_value -= digit * multiplier
            digit = inverse_map[-1 * digit]
        digits.append(str(digit))

    return "".join(digits)


total_sum = 0

map = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}
inverse_map = {v: k for (k, v) in map.items()}

# print(to_snafu(2022))
# print(to_snafu(12345))
# print(to_snafu(314159265))
# exit()

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        value = 0
        for (index, char) in enumerate(line[::-1]):
            multiplier = pow(5, index)
            value += multiplier * map[char]
        total_sum += value
print(total_sum)
print(to_snafu(total_sum))
