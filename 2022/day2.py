rounds = []

with open("input.txt") as f:
    for row in f:
        row = row.strip()
        a, b = row.split(" ")
        rounds.append((a, b))


MAP = {
    "X": "A",
    "Y": "B",
    "Z": "C"
}
SCORE_WIN = {
    "X": 0,
    "Y": 3,
    "Z": 6
}
SCORE_CHOOSE = {
    "A": 1,
    "B": 2,
    "C": 3
}


def get_key(input: str, index: int):
    keys = list(SCORE_CHOOSE.keys())
    index += keys.index(input)
    return keys[(index + len(keys)) % len(keys)]


def calculate_score(a, b):
    score = SCORE_WIN[b]

    if b == "Y":
        score += SCORE_CHOOSE[a]
    elif b == "X":
        index = get_key(a, -1)
        score += SCORE_CHOOSE[index]
    elif b == "Z":
        index = get_key(a, 1)
        score += SCORE_CHOOSE[index]
    return score


print(sum(calculate_score(a, b) for (a, b) in rounds))
