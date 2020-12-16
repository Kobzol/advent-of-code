import functools
import re
from collections import defaultdict


def is_valid(constraint, value):
    a1, a2 = constraint[0]
    b1, b2 = constraint[1]
    if a1 <= value <= a2 or b1 <= value <= b2:
        return True
    return False


constraint_regex = re.compile(r"(.+?): (\d+)-(\d+) or (\d+)-(\d+)")

constraints = {}
my_ticket = None
other_tickets = []

with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]

    index = 0
    for line in lines:
        index += 1
        if not line:
            break
        match = constraint_regex.match(line)
        assert match
        name, a1, a2, b1, b2 = match.groups()
        assert name not in constraints
        constraints[name] = (
            (int(a1), int(a2)),
            (int(b1), int(b2))
        )

    lines = lines[index + 1:]
    my_ticket = [int(x) for x in lines[0].split(",")]
    for line in lines[3:]:
        ticket = [int(x) for x in line.split(",")]
        other_tickets.append(ticket)

valid_tickets = []
for ticket in other_tickets:
    for value in ticket:
        if not any(is_valid(constraint, value) for constraint in constraints.values()):
            break
    else:
        valid_tickets.append(ticket)


slots = defaultdict(list)
for slot in range(len(my_ticket)):
    for (name, constraint) in constraints.items():
        for ticket in valid_tickets:
            if not is_valid(constraint, ticket[slot]):
                break
        else:
            slots[slot].append(name)
slots = dict(slots)
slots = sorted(slots.items(), key=lambda x: len(x[1]))


def create_schedule(tickets, schedule, slot):
    if slot == len(my_ticket):
        return schedule

    index, constraint_names = slots[slot]
    for constraint_name in constraint_names:
        if constraint_name in schedule:
            continue
        next_schedule = dict(schedule)
        next_schedule[constraint_name] = index
        final = create_schedule(tickets, next_schedule, slot + 1)
        if final is not None:
            return final
    return None


schedule = create_schedule(valid_tickets, {}, 0)
result = [my_ticket[v] for (k, v) in schedule.items() if k.startswith("departure")]
print(functools.reduce(lambda a, b: a * b, result))
