with open("input.txt") as f:
    input = f.read().strip()


length = 14


def iterate():
    for i in range(len(input) - length - 1):
        yield input[i:i+length]



for (index, item) in enumerate(iterate()):
    if len(set(item)) == length:
        print(index + length)
        break
