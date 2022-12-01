elves = []
calories = 0

with open("input.txt") as f:
    for row in f:
        row = row.strip()
        if row == "":
            elves.append(calories)
            calories = 0
        else:
            calories += int(row)

elves.append(calories)

print(sum(sorted(elves, reverse=True)[:3]))
