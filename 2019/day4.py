def is_valid(i):
    s = str(i)
    if len(s) != 6:
        return False
    for i in range(len(s) - 1):
        if int(s[i]) > int(s[i + 1]):
            return False
    runs = {}
    last = None
    count = 0
    for i in s:
        if i != last:
            if last is not None:
                runs[last] = count
            last = i
            count = 0
        count += 1
    runs[last] = count

    return any(x == 2 for x in runs.values())


counter = 0

for i in range(137683, 596253 + 1):
    if is_valid(i):
        counter += 1

print(counter)
