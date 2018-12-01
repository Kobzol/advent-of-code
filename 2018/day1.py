freq = 0
freqs = {}

nums = []

with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        num = int(line)
        nums.append(num)


i = 0
while True:
    if freq in freqs:
        print(freq)
        exit()
    freqs[freq] = 1
    freq += nums[i % len(nums)]
    i += 1
