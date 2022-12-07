import collections
from pathlib import Path
from typing import Dict, Optional


class Node:
    def __init__(self, parent: Optional["Node"]):
        self.parent = parent

    def size(self) -> int:
        raise NotImplementedError()

    def iterate(self):
        return
        yield


class Directory(Node):
    def __init__(self, path: Path, parent: Optional["Node"]):
        super().__init__(parent)
        self.path = path
        self.nodes: Dict[str, Node] = {}

    def iterate(self):
        for node in self.nodes.values():
            yield node
            yield from node.iterate()

    def size(self) -> int:
        return sum(node.size() for node in self.nodes.values())

    def add_dir(self, name: str) -> "Directory":
        if name not in self.nodes:
            self.nodes[name] = Directory(self.path / name, self)
        return self.nodes[name]

    def add_file(self, name: str, size: int) -> "File":
        if name not in self.nodes:
            self.nodes[name] = File(self.path / name, size, self)
        return self.nodes[name]

    def __repr__(self):
        return f"Dir(path={self.path})"


class File(Node):
    def __init__(self, path: Path, size: int, parent: Optional["Node"]):
        super().__init__(parent)
        self.path = path
        self._size = size

    def size(self) -> int:
        return self._size

    def __repr__(self):
        return f"File(name={self.path.name}, size={self.size()})"


class Filesystem:
    def __init__(self):
        self.root = Directory(Path("/"), parent=None)
        self.current: Directory = self.root

    def traverse(self, lines: collections.deque[str]):
        line = lines.popleft()
        if line.startswith("$"):
            line = line[2:]
            if line == "cd /":
                self.current = self.root
            elif line == "cd ..":
                self.current = self.current.parent
                assert self.current is not None
            elif line.startswith("cd"):
                dir = line[3:]
                self.current = self.current.add_dir(dir)
            elif line == "ls":
                while lines:
                    row = lines.popleft()
                    if row.startswith("$"):
                        lines.appendleft(row)
                        break
                    if row.startswith("dir"):
                        self.current.add_dir(row[4:])
                    else:
                        size, name = row.split()
                        self.current.add_file(name=name, size=int(size))

        return lines


output = []
with open("input.txt") as f:
    for line in f:
        output.append(line.strip())

output = collections.deque(output)
fs = Filesystem()
while output:
    fs.traverse(output)

total_disk = 70000000
unused_needed = 30000000
used = fs.root.size()
print(used)
to_remove = unused_needed - (total_disk - used)
print(to_remove)
dirs = [node for node in fs.root.iterate() if isinstance(node, Directory) and node.size() >= to_remove]
dirs = sorted(dirs, key=lambda d: d.size())
print(dirs[0].size())
