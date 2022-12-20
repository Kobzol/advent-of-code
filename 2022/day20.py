import dataclasses
from typing import Dict, List, Optional, Tuple

import tqdm

numbers = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        numbers.append(int(line) * 811589153)


@dataclasses.dataclass
class LinkedList:
    value: int
    prev: Optional["LinkedList"] = None
    next: Optional["LinkedList"] = None

    def find(self, value: int) -> "LinkedList":
        first = self
        current = first
        while True:
            if current.value == value:
                return current
            current = current.next
            if current == first:
                assert False

    def swap_next(self):
        prev = self.prev
        next = self.next
        next_next = next.next
        prev.next = next
        next.prev = prev
        next.next = self
        self.prev = next
        self.next = next_next
        next_next.prev = self

    def swap_prev(self):
        prev = self.prev
        next = self.next
        prev_prev = prev.prev
        next.prev = prev
        prev.next = next
        prev.prev = self
        self.prev = prev_prev
        self.next = prev
        prev_prev.next = self

    def offset_after(self, n: int) -> "LinkedList":
        current = self
        for _ in range(abs(n)):
            if n > 0:
                current = current.next
            else:
                current = current.prev
        if n < 0:
            current = current.prev
        return current

    def swap(self, other: "LinkedList"):
        sp = self.prev
        sn = self.next
        op = other.prev
        on = other.next

        sp.next = other
        other.prev = sp
        sn.prev = other
        other.next = sn

        op.next = self
        self.prev = op
        on.prev = self
        self.next = on

    def move_after(self, after: "LinkedList"):
        if after is self:
            return
        sp = self.prev
        sn = self.next
        sp.next = sn
        sn.prev = sp

        an = after.next
        after.next = self
        self.prev = after
        self.next = an
        an.prev = self

    def sanity_check(self):
        count = 0
        first = self
        current = first
        while True:
            count += 1
            if count > len(numbers):
                assert False
            current = current.next
            if current == first:
                break
        assert count == len(numbers)


def lst_to_linked(items: List[int]) -> Tuple[LinkedList, List[LinkedList]]:
    nodes = []
    prev = LinkedList(value=items[0])
    nodes.append(prev)
    first = prev
    next_item = first
    for item in items[1:]:
        next_item = LinkedList(value=item, prev=prev, next=None)
        prev.next = next_item
        prev = next_item
        nodes.append(next_item)
    next_item.next = first
    first.prev = next_item
    assert linked_to_lst(first) == items
    return (first, nodes)


def linked_to_lst(items: LinkedList) -> List[int]:
    values = []
    first = items
    current = first
    while True:
        values.append(current.value)
        current = current.next
        if current == first:
            break
    return values


def swap(items: List[int], a: int, b: int):
    a = (a + len(items)) % len(items)
    b = (b + len(items)) % len(items)
    x = items[a]
    items[a] = items[b]
    items[b] = x


def swap_lists():
    nums2 = list(numbers)
    offset = 0
    for number in tqdm.tqdm(numbers):
        index = nums2.index(number)
        target_index = ((index + number) + len(numbers)) % len(numbers)
        to_move = number
        if number < 0:
            for _ in range(abs(to_move)):
                if index == 0:
                    nums2.append(nums2.pop(0))
                    index = len(nums2) - 1
                swap(nums2, index - 1, index)
                index -= 1
                if index == 0:
                    nums2.append(nums2.pop(0))
                    index = len(nums2) - 1
        else:
            for _ in range(to_move):
                if index == len(nums2) - 1:
                    nums2.insert(0, nums2.pop())
                    index = 0
                swap(nums2, index + 1, index)
                index += 1
                if index == len(nums2) - 1:
                    nums2.insert(0, nums2.pop())
                    index = 0
        # print(nums2)


def get_index(items: List[int], index: int) -> int:
    return items[(items.index(0) + index) % len(items)]


map: Dict[int, List[LinkedList]] = {}
(linked, items) = lst_to_linked(numbers)

for _ in range(10):
    for item in tqdm.tqdm(items):
        # item.move_after(item.offset_after(item.value))
        to_move = abs(item.value) % (len(numbers) - 1)
        for _ in range(to_move):
            if item.value > 0:
                item.swap_next()
            else:
                item.swap_prev()
        """
        item.move_after(item.offset_after(number))
        #linked.sanity_check()
        """

nums = linked_to_lst(linked)
assert set(nums) == set(numbers)
print(nums)
print(get_index(nums, 1000) + get_index(nums, 2000) + get_index(nums, 3000))

# 21319 too high
# 16569 too high
# 1753
# 3112
# 3992
# -331?
# 98?
# 7153
# 14626
