with open("input.txt") as f:
    input = f.read().strip()
skip = int(input[:7])
input = [int(v) for v in input] * 10000
input = input[skip:]

pattern = (0, 1, 0, -1)


for _ in range(100):
    cumsum = 0
    for i in range(len(input)):
        position = len(input) - i - 1
        cumsum += input[position]
        input[position] = abs(cumsum) % 10

input = input[:8]
print("".join(str(v) for v in input))
