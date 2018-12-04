import numpy as np

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

entries = []

for line in lines:
    data = line.split(" ")
    year = data[0][6:]
    hour = data[1][:5]
    entries.append((year, hour, data[2:]))

entries = sorted(entries, key=lambda k: (k[0], k[1]))

guards = {}
guard = None
for (day, time, data) in entries:
    if len(data) == 4:
        guard = data[1]
        guards.setdefault(guard, [])
    elif data == ["falls", "asleep"]:
        guards[guard].append([int(time.split(":")[1])])
    elif data == ["wakes", "up"]:
        guards[guard][-1].append(int(time.split(":")[1]))

def s(x):
    return sum([t - f for (f, t) in x[1]])

values = guards.items()
values = sorted(values, key=lambda i: s(i), reverse=True)

def get_hist(values):
    histogram = np.zeros(60)
    for (f, t) in values:
        histogram[f:t+1] += 1
    return np.max(histogram), np.argmax(histogram)

data = []
for (guard, val) in values:
    data.append((guard, get_hist(val)))

data = sorted(data, key=lambda x:x[1][0], reverse=True)
print(data)
