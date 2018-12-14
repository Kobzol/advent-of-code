iters = 380621
iter_str = str(iters)

elves = [0, 1]
recipes = [3, 7]


def get_digits(num):
    if num == 0:
        return [0]

    digits = []
    while num > 0:
        digits.append(num % 10)
        num //= 10
    return reversed(digits)


while True:
    s = recipes[elves[0]] + recipes[elves[1]]
    recipes += get_digits(s)
    for i, e in enumerate(elves):
        next = (e + 1 + recipes[e]) % len(recipes)
        elves[i] = next
    if len(recipes) >= len(iter_str):
        if str(recipes[-1]) == iter_str[-1] or str(recipes[-2]) == iter_str[-1]:
            for i in range(2):
                if len(iter_str) + i <= len(recipes):
                    start = len(recipes)-len(iter_str)-i
                    st = "".join(map(str, recipes[start:start+len(iter_str)]))
                    if st == iter_str:
                        print("match")
                        print(len(recipes) - len(iter_str) - i)
                        exit(0)
