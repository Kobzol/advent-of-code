players = 476
marbles = (71431 * 100) + 1


class Node:
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next or self
        self.prev = prev or self

    def index(self, index):
        tar = self
        for i in range(abs(index)):
            tar = tar.prev if index < 0 else tar.next
        return tar

    def insert_after(self, value):
        node = Node(value, self.next, self)
        next = self.next
        self.next = node
        next.prev = node
        return node

    def remove(self):
        assert self.prev != self
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.next

    def __str__(self):
        return str(self.value)


circle = Node(0)
first = circle
player = 0
scores = [0] * players

for i in range(1, marbles):
    if i % 23 == 0:
        scores[player] += i
        tar = circle.index(-7)
        scores[player] += tar.value
        circle = tar.remove()
    else:
        current_index = circle.index(1)
        if current_index == first:
            current_index = circle.index(1)
        circle = current_index.insert_after(i)

    player = (player + 1) % players

print(max(scores))
