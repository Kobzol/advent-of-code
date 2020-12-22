import collections

players = []

player = -1
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if line.startswith("Player"):
            player += 0
            players.append(collections.deque())
        elif line.isdigit():
            players[player].append(int(line))


def play(players, visited):
    while all(players):
        key = (tuple(players[0]), tuple(players[1]))
        if key in visited:
            return 0, players[0]
        visited.add(key)

        # print(f"Decks: {players}")
        cards = [player.popleft() for player in players]
        if all(cards[c] <= len(players[c]) for c in range(2)):
            new_decks = [collections.deque(list(players[c])[:cards[c]]) for c in range(2)]
            winner, _ = play(new_decks, set())
        else:
            winner = 0 if cards[0] > cards[1] else 1
        # print(f"Winner: {winner}")
        players[winner].append(cards[winner])
        players[winner].append(cards[1 - winner])

    winner = 0 if players[0] else 1
    return winner, players[winner]


winner, deck = play(players, set())
score = sum((index + 1) * value for (index, value) in enumerate(reversed(deck)))
print(score)

# 31680 too low
