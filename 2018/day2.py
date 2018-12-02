with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

a = 0
b = 0

for line in lines:
    for line2 in lines:
        if len(line) == len(line2):
            x = 0
            j = 0
            for i, (a, b) in enumerate(zip(line, line2)):
                if a != b:
                    x += 1
                    j = i
            if x == 1:
                print(line)
                print(line2)
                print(line[:j] + line[j + 1:])
