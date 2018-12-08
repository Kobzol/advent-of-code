with open("input.txt", "r") as f:
    data = [int(x) for x in f.read().strip().split(" ")]


def parse(i):
    children = data[i]
    metadata = data[i + 1]
    index = i + 2
    total = 0
    children_values = []
    for x in range(children):
        index, sumchild = parse(index)
        total += sumchild
        children_values.append(sumchild)
    for x in range(metadata):
        total += data[index + x]

    value = 0
    if not children:
        value = sum(data[index:index+metadata])
    else:
        for i in range(metadata):
            met = data[index + i]
            if met > 0:
                met -= 1
                if met < len(children_values):
                    value += children_values[met]
    return index + metadata, value


print(parse(0))
