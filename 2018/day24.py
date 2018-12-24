import copy
import re

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

"""groups = [
    [0, 17, 5390, 2, 4507, "fire", {
        "radiation": 2.0,
        "bludgeoning": 2.0
    }, 1],
    [0, 989, 1274, 3, 25, "slashing", {
        "fire": 0.0,
        "bludgeoning": 2.0,
        "slashing": 2.0
    }, 2],
    [1, 801, 4706, 1, 116, "bludgeoning", {
        "radiation": 2.0
    }, 3],
    [1, 4485, 2961, 4, 12, "slashing", {
        "radiation": 0.0,
        "fire": 2.0,
        "cold": 2.0
    }, 4]
]"""
groups = []

team = 0
for line in lines:
    if line.startswith("Infection"):
        team += 1
    if not line or not line[0].isdigit():
        continue
    units = int(line[:line.index(" ")])
    line = line[line.index("each with ") + 10:]
    hp = int(line[:line.index(" ")])
    modifier_map = {}
    if "(" in line:
        line = line[line.index("(") + 1:]
        modifiers = line[:line.index(")")]
        weak = re.compile("weak to ((?:\w+(?:, )?)*)")
        weak = weak.findall(modifiers)
        if weak:
            for t in weak[0].split(","):
                modifier_map[t.strip()] = 2.0

        immune = re.compile("immune to ((?:\w+(?:, )?)*)")
        immune = immune.findall(modifiers)
        if immune:
            for t in immune[0].split(","):
                modifier_map[t.strip()] = 0.0

    line = line[line.index("that does ") + 10:]
    attack = int(line[:line.index(" ")])
    line = line[line.index(" ") + 1:]
    attack_type = line[:line.index(" ")]
    line = line[line.index("initiative ") + 11:]
    init = int(line.strip())
    groups.append([team, units, hp, init, attack, attack_type, modifier_map, len(groups)])


def groupid(group):
    return group[7]


def eff_power(group):
    return group[1] * group[4]


def initiative(group):
    return group[3]


def dmg_count(attacker, defender):
    power = eff_power(attacker)
    attack_type = attacker[5].strip()
    modifier = defender[6].get(attack_type, 1.0)
    return int(power * modifier)


def find_group(id):
    ret = [g for g in groups if groupid(g) == id]
    assert len(ret) == 1
    return ret[0]


def fight(boost):
    global groups
    for g in groups:
        if g[0] == 0:
            g[4] += boost

    counter = 0
    while len(set(g[0] for g in groups)) > 1:
        targets = {}
        assert all(g[1] > 0 for g in groups)
        local = sorted(groups, key=lambda g: (eff_power(g), initiative(g)), reverse=True)
        for group in local:
            target = sorted([g for g in groups if g[0] != group[0] and groupid(g) not in targets.values()],
                            key=lambda g: (dmg_count(group, g), eff_power(g), initiative(g)), reverse=True)
            if target:
                assert target[0][1] > 0
                if dmg_count(group, target[0]) == 0:
                    continue
                assert groupid(group) not in targets
                assert groupid(target[0]) not in targets.values()
                targets[groupid(group)] = groupid(target[0])
        battles = sorted(targets.items(), key=lambda g: initiative(find_group(g[0])), reverse=True)
        removed = set()
        attacked = set()
        for (att, defender) in battles:
            assert defender not in removed
            assert defender not in attacked
            attacked.add(defender)

            att = find_group(att)
            defender = find_group(defender)

            assert defender[1] > 0
            if groupid(att) not in removed:
                assert att[1] > 0
                dmg = dmg_count(att, defender)
                dmg //= defender[2]
                defender[1] -= dmg
                if defender[1] <= 0:
                    removed.add(groupid(defender))
        groups = [g for g in groups if groupid(g) not in removed]
        counter += 1
        if counter % 1000 == 0:
            print(boost, counter)
        if counter > 100000:
            return None

    if all(g[0] == 0 for g in groups):
        return sum(g[1] for g in groups)
    return None


orig_groups = copy.deepcopy(groups)
boost = 0
while True:
    groups = copy.deepcopy(orig_groups)
    ret = fight(boost)
    if ret is not None:
        print(ret)
        break
    print(boost)
    boost += 1
