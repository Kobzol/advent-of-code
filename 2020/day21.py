from collections import Counter

ingredient_counter = Counter()
allergen_map = {}

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        allergen_start = line.index("(")
        if allergen_start == -1:
            allergen_start = len(line)
        ingredients = line[:allergen_start].strip().split()
        for ingredient in ingredients:
            ingredient_counter[ingredient] += 1
        allergens = line[allergen_start + 10:-1].split(", ")
        for allergen in allergens:
            if allergen not in allergen_map:
                allergen_map[allergen] = set(ingredients)
            else:
                allergen_map[allergen] &= set(ingredients)

valid_ingredients = set(ingredient_counter.keys())
for (allergen, ingredients) in allergen_map.items():
    valid_ingredients -= ingredients

print(sum(ingredient_counter[i] for i in valid_ingredients))

allergens = sorted(allergen_map.items(), key=lambda v: len(v[1]))
allergen_count = len(allergens)


def assign(allergens, assignments, taken):
    if len(assignments) == allergen_count:
        return assignments

    allergen, ingredients = allergens[0]
    possible_ingredients = ingredients - taken
    for item in possible_ingredients:
        assignments2 = dict(assignments)
        assignments2[allergen] = item
        taken2 = set(taken)
        taken2.add(item)
        ret = assign(allergens[1:], assignments2, taken2)
        if ret is not None:
            return ret
    return None


assignments = assign(allergens, {}, set())
assigned = sorted(assignments.items(), key=lambda v: v[0])
assigned = ",".join([v[1] for v in assigned])
print(assigned)
print(assignments)

# xgtj,mdbq,jdggtft,rmd,ztdctgq wrong
