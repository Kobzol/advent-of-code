import re

bag_re = re.compile(r"((\d) (.*?)) bag")


def bag_contains(needle, bag, bag_sets, visited):
    if bag == needle:
        return True
    if bag in visited:
        return False
    visited.add(bag)
    for b in bag_sets[bag]:
        if bag_contains(needle, b, bag_sets, visited):
            return True
    return False


def count_bags(needle, bag_sets, cache):
    if needle in cache:
        return cache[needle]
    count = 0
    for (component, needed_count) in bag_sets[needle]:
        count += count_bags(component, bag_sets, cache) * needed_count
    return count + 1


bag_sets = {}
with open("input.txt") as f:
    for row in f:
        line = row.strip()
        name = line[:line.index("bags") - 1]
        line = line[len(name) + 14:]
        components = [(m[2], int(m[1])) for m in bag_re.findall(line)]
        assert name not in bag_sets
        bag_sets[name] = components


print(count_bags("shiny gold", bag_sets, {}) - 1)
