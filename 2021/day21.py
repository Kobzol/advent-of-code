from collections import Counter
from typing import List

# players = [4, 8]
players = [1, 6]
players = [p - 1 for p in players]
scores = [0, 0]


def deterministic_dice():
    while True:
        for i in range(1, 101):
            yield i


def play() -> int:
    dice = deterministic_dice()
    rolled = 0
    while True:
        for player in range(2):
            move_amount = sum(next(dice) for _ in range(3))
            rolled += 3

            position = (players[player] + move_amount) % 10
            players[player] = position
            score = position + 1
            scores[player] += score
            if scores[player] >= 1000:
                return rolled * scores[1 - player]


dice_values = Counter()

for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            dice_values[i + j + k] += 1

winned = [0, 0]


def play_quantum(player: int, players: List[int], scores: List[int], universe_count: int):
    for p in range(2):
        if scores[p] >= 21:
            winned[p] += universe_count
            return

    for (value, num_universes) in dice_values.items():
        players_next = list(players)
        players_next[player] = (players_next[player] + value) % 10
        score = players_next[player] + 1
        scores_next = list(scores)
        scores_next[player] += score
        play_quantum(1 - player, players_next, scores_next, universe_count * num_universes)


play_quantum(0, players, [0, 0], 1)
print(winned)
