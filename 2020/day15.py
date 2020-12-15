import collections

occur = collections.defaultdict(lambda: collections.deque(maxlen=2))

numbers = [18, 8, 0, 5, 4, 1, 20]

index = 0
for number in numbers:
    occur[number].append(index)
    index += 1

last = numbers[-1]
while index < 30000000:
    if len(occur[last]) < 2:
        number = 0
    else:
        number = occur[last][1] - occur[last][0]
    occur[number].append(index)
    last = number
    index += 1

print(last)
