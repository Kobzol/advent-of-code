import tqdm as tqdm


class Node:
    def __init__(self, id):
        self.id = id
        self.prev = None
        self.next = None

    def iterate_next(self, count):
        node = self.next
        for _ in range(count):
            yield node
            node = node.next

    def join(self, other):
        self.next = other
        other.prev = self

    def __str__(self):
        return f"{self.id}: [{self.prev.id}, {self.next.id}]"


input = "167248359"
min_id = 1
items = []
id_to_node = {}

for (index, c) in enumerate(input):
    items.append(Node(int(c)))

for i in range(1000000 - len(input)):
    items.append(Node(i + len(input) + 1))

for (index, node) in enumerate(items):
    id_to_node[node.id] = node
    prev_index = ((index - 1) + len(items)) % len(items)
    next_index = (index + 1) % len(items)
    node.prev = items[prev_index]
    node.next = items[next_index]

max_id = len(items)
total_count = max_id


def iterate_wrap(start, count, dir, min, max):
    for i in range(count):
        if start > max:
            start = min
        elif start < min:
            start = max
        yield start
        start += dir


def iterate_ids(start, count, dir):
    yield from iterate_wrap(start, count, dir, min_id, max_id)


def find_id(items, id):
    return items.index(id)


def move(current_node):
    node_next = []
    node_next_ids = []
    for node in current_node.iterate_next(3):
        node_next.append(node)
        node_next_ids.append(node.id)

    dest_id = None
    for destination_id in iterate_ids(current_node.id - 1, total_count, -1):
        if destination_id not in node_next_ids:
            dest_id = destination_id
            break
    assert dest_id is not None
    # print("Pick up", node_next_ids, "Destination", dest_id)

    current_node.join(node_next[-1].next)

    dest_node = id_to_node[dest_id]
    dest_node_next = dest_node.next
    dest_node.join(node_next[0])
    node_next[-1].join(dest_node_next)

    return current_node.next


current_node = items[0]
for i in tqdm.tqdm(range(10000000)):
    # print([node.id for node in items[0].iterate_next(total_count)])
    current_node = move(current_node)
    # print()

a, b = list(id_to_node[1].iterate_next(2))
print(a.id * b.id)
