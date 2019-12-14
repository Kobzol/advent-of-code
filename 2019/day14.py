import math

ingredients = {}
items = set()

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        l, r = line.split(" => ")

        def parse(x):
            count, item = x.split(" ")
            count = int(count)
            items.add(item)
            return (item, count)

        requirements = dict(parse(item) for item in l.split(", "))
        count, target = r.split(" ")
        items.add(target)
        count = int(count)
        ingredients[target] = {
            "count": count,
            "requirements": requirements
        }


def solve_leftover(key, count, leftovers):
    if key == "ORE":
        return count

    if key in leftovers:
        leftover_take = min(leftovers[key], count)
        leftovers[key] -= leftover_take
        count -= leftover_take

    if count == 0:
        return 0

    item = ingredients[key]
    multiplier = math.ceil(count / item["count"])
    real_count = multiplier * item["count"]
    leftover_count = real_count - count
    total = 0
    requirements = dict(item["requirements"])

    for (req, req_count) in requirements.items():
        total += solve_leftover(req, req_count * multiplier, leftovers)

    leftovers[key] += leftover_count

    return total


def solve(key, count, result):
    item = ingredients[key]
    multiplier = math.ceil(count / item["count"])
    print(count, item["count"], multiplier)
    assert multiplier * item["count"] >= count
    requirements = dict(item["requirements"])

    if "ORE" in requirements:
        assert len(requirements) == 1
        if key not in result:
            result[key] = 0
        result[key] += count
    else:
        for _ in range(multiplier):
            for (req, req_count) in requirements.items():
                solve(req, req_count, result)


def get_ores(item, count):
    ore_per_item = ingredients[item]["requirements"]["ORE"]
    count_per_item = ingredients[item]["count"]
    real_count = math.ceil(count / count_per_item)
    return real_count * ore_per_item


print(ingredients)
assert ingredients["FUEL"]["count"] == 1

maximum_ore = 1000000000000
fuel_count = 1
min_fuel_count = 1
max_fuel_count = 10000000

while min_fuel_count < max_fuel_count:
    leftovers = {item: 0 for item in items}
    index = (min_fuel_count + max_fuel_count) // 2
    ore_result = solve_leftover("FUEL", index, leftovers)
    if ore_result < maximum_ore:
        min_fuel_count = index + 1
    else:
        max_fuel_count = index
    print(index, ore_result, ore_result / maximum_ore)

"""result = {}
solve("FUEL", 1, result)

print(result)
s = sum(get_ores(item, count) for (item, count) in result.items())
print(s)"""

# 817248 too low
# 1665990 too high
