import re
import itertools

height_regex = re.compile(r"^(\d+)(cm|in)$")
hcl_regex = re.compile(r"^#([0-9a-f]){6}$")

valid = 0

needed_keys = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
]


def validate(passport):
    try:
        assert all(k in passport for k in needed_keys)
        assert 1920 <= int(passport["byr"]) <= 2002
        assert 2010 <= int(passport["iyr"]) <= 2020
        assert 2020 <= int(passport["eyr"]) <= 2030
        match = height_regex.match(passport["hgt"])
        assert match
        height, count = match.groups()
        assert count in ("cm", "in")
        if count == "cm":
            assert 150 <= int(height) <= 193
        else:
            assert 59 <= int(height) <= 76
        assert hcl_regex.match(passport["hcl"])
        assert passport["ecl"] in "amb blu brn gry grn hzl oth".split(" ")
        assert re.compile(r"^(\d){9}$").match(passport["pid"])
    except:
        return False
    return True


with open("input.txt") as f:
    passport = {}
    for row in f:
        line = row.strip()
        if not line:
            if validate(passport):
                valid += 1
            passport = {}
        else:
            for item in line.split(" "):
                key, value = item.split(":")
                assert key not in passport
                passport[key] = value
    if passport and validate(passport):
        valid += 1

print(valid)
