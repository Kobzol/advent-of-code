import re

regex = re.compile(r"(\d+)-(\d+) (\w): (.*)")

valid = 0

with open("input.txt") as f:
    for row in f:
        line = row.strip()
        match = regex.match(line)
        assert match
        minimum = int(match.group(1)) - 1
        maximum = int(match.group(2)) - 1
        char = match.group(3)
        password = match.group(4)
        a = password[minimum]
        b = password[maximum]
        if (a == char or b == char) and a != b:
            valid += 1

print(valid)
