import math


def transform(subject, loop_size):
    state = 1
    for _ in range(loop_size):
        state *= subject
        state %= 20201227
    return state


def find_count(target):
    loop_size = 1
    state = 1
    while True:
        state *= 7
        state %= 20201227
        if state == target:
            return loop_size
        loop_size += 1


def find_count2(target):
    x = 0
    log_7 = math.log2(7)
    while True:
        r = x * 20201227 + target
        source = math.log2(r) / log_7

        print(source, int(source))
        if source == int(source):
            return int(source)
        x += 1


public_keys = [18499292, 8790390]
# public_keys = [5764801, 17807724]
loops = [find_count(k) for k in public_keys]
print(loops)
encryption_keys = [transform(pk, loop) for (pk, loop) in zip(reversed(public_keys), loops)]
assert encryption_keys[0] == encryption_keys[1]
print(encryption_keys[0])
