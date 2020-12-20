import functools
import math
from collections import defaultdict

import numpy as np
import cv2


def get_variants(data):
    yield data
    yield cv2.flip(data, 1)
    yield cv2.flip(data, 0)

    ref = data
    for i in range(3):
        ref = cv2.rotate(ref, cv2.cv2.ROTATE_90_CLOCKWISE)
        yield ref
        yield cv2.flip(ref, 1)
        yield cv2.flip(ref, 0)


def to_numpy(data, a, b):
    return np.array([1 if c == "#" else 0 for c in data]).reshape((a, b))


def parse_numpy(lines):
    tile_data = []
    tile_dim = None
    for line in lines.splitlines(keepends=False):
        tile_dim = len(line)
        tile_data.extend(line)
    return (tile_dim, tile_data)


with open("input.txt") as f:
    tile_dim, input_data = parse_numpy(f.read())
    input_data = to_numpy(input_data, tile_dim, tile_dim)

sea_monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
monster_tile_dim, monster_data = parse_numpy(sea_monster)
monster_data = to_numpy(monster_data, 3, monster_tile_dim)
s_height, s_width = monster_data.shape

for (v_index, variant) in enumerate(get_variants(input_data)):
    rows, cols = variant.shape
    valid_hashes = set()
    for row in range(rows):
        for col in range(cols):
            if variant[row, col] == 1:
                valid_hashes.add((row, col))
    found = False
    for row in range((rows - s_height) + 1):
        for col in range((cols - s_width) + 1):
            grid = variant[row:row + s_height, col:col + s_width]
            if ((monster_data & grid) == monster_data).all():
                found = True
                for r in range(s_height):
                    for c in range(s_width):
                        if monster_data[r, c] == 1:
                            r1 = row + r
                            c1 = col + c
                            pos = (r1, c1)
                            if pos in valid_hashes:
                                valid_hashes.remove(pos)
    if found:
        print(len(valid_hashes))

exit()
# Part 1


class Tile:
    TILE_DIM = 10

    def __init__(self, id, variants):
        self.id = id
        self.variants = list(variants)
        self.possible_locations = [set() for _ in range(len(self.variants))]

    def is_possible(self, variant, pos, square_size):
        row, col = pos
        possible = self.possible_locations[variant]
        if row == 0 and "top" in possible:
            return False
        elif row == square_size - 1 and "bottom" in possible:
            return False
        elif col == 0 and "left" in possible:
            return False
        elif col == square_size - 1 and "right" in possible:
            return False
        elif 0 < row < square_size - 1 and 0 < col < square_size - 1 and len(possible) != 4:
            return False
        return True

    def to_str(self, variant):
        items = ["#" if c == 1 else "." for c in self.variants[variant].flatten()]
        string = f"{self.id}\n"
        index = 0
        for row in range(Tile.TILE_DIM):
            for col in range(Tile.TILE_DIM):
                string += items[index]
                index += 1
            string += "\n"
        return string

    def get_data(self, variant):
        return self.variants[variant]

    def get_variants(self):
        for i in range(len(self.variants)):
            yield i

    def get_edge(self, variant, type):
        data = self.get_data(variant)
        if type == "top":
            return data[0]
        elif type == "bottom":
            return data[-1]
        elif type == "left":
            return data[:, 0]
        elif type == "right":
            return data[:, -1]
        else:
            assert False


def match_edges(t1, t2, t1_variant, t2_variant, t1_edge, t2_edge):
    value = np.array_equal(t1.get_edge(t1_variant, t1_edge), t2.get_edge(t2_variant, t2_edge))
    return value


def match_two_tiles(t1, t2, t1_variant, t2_variant):
    matches = set()
    if match_edges(t1, t2, t1_variant, t2_variant, "top", "bottom"):
        matches.add("top")
    if match_edges(t1, t2, t1_variant, t2_variant, "right", "left"):
        matches.add("right")
    if match_edges(t1, t2, t1_variant, t2_variant, "bottom", "top"):
        matches.add("bottom")
    if match_edges(t1, t2, t1_variant, t2_variant, "left", "right"):
        matches.add("left")
    return matches


class State:
    def __init__(self, position, locations, remaining):
        pass


tiles = []
parsing_tile = False
tile_id = None
tile_data = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if line.startswith("Tile"):
            tile_id = int(line[5:-1])
            parsing_tile = True
        elif parsing_tile:
            if not line:
                assert tile_id is not None
                tiles.append(Tile(tile_id, get_variants(to_numpy(tile_data))))
                parsing_tile = False
                tile_id = None
                tile_data = []
            else:
                tile_data.extend(line)


assert tile_id is not None
assert parsing_tile
tiles.append(Tile(tile_id, get_variants(to_numpy(tile_data))))

print(f"Tile count: {len(tiles)}")
square_size = int(math.sqrt(len(tiles)))
print(f"Image size: {square_size}")

left_right_initial = set()
for t1 in tiles:
    for v1 in t1.get_variants():
        matches = set()
        for t2 in tiles:
            if t1 == t2:
                continue
            for v2 in t2.get_variants():
                matches |= match_two_tiles(t1, t2, v1, v2)
        if matches == {"right", "bottom"}:
            left_right_initial.add((t1, v1))
        t1.possible_locations[v1] = matches

POSITIONS = ["top", "right", "bottom", "left"]
OPPOSITE = {
    "top": "bottom",
    "right": "left",
    "bottom": "top",
    "left": "right"
}
VALID_AT = defaultdict(list)
for row in range(square_size):
    for col in range(square_size):
        for t1 in tiles:
            for v1 in t1.get_variants():
                if t1.is_possible(v1, (row, col), square_size):
                    VALID_AT[(row, col)].append((t1, v1))


def move_position(pos, vec):
    if vec == "top":
        return (pos[0] - 1, pos[1])
    elif vec == "right":
        return (pos[0], pos[1] + 1)
    elif vec == "bottom":
        return (pos[0] + 1, pos[1])
    elif vec == "left":
        return (pos[0], pos[1] - 1)
    else:
        assert False


def is_valid_position(position):
    return 0 <= position[0] < square_size and 0 <= position[1] < square_size


def postprocess(locations):
    canvas_size = (Tile.TILE_DIM - 2) * square_size
    canvas = ['' for _ in range(canvas_size * canvas_size)]
    for row in range(square_size):
        for col in range(square_size):
            tile, variant = locations[(row, col)]
            data = tile.get_data(variant)
            without_gaps = data[1:-1, 1:-1]
            for r in range(Tile.TILE_DIM - 2):
                for c in range(Tile.TILE_DIM - 2):
                    r1 = row * (Tile.TILE_DIM - 2) + r
                    c1 = col * (Tile.TILE_DIM - 2) + c
                    canvas[r1 * canvas_size + c1] = without_gaps[r, c]
    for row in range(canvas_size):
        for col in range(canvas_size):
            value = canvas[row * canvas_size + col]
            item = "#" if value == 1 else "."
            print(item, end="")
        print()
    exit()


def find(data, position, locations, remaining):
    tile, variant = data

    if len(remaining) == 0:
        for row in range(square_size):
            for col in range(square_size):
                t, v = locations[(row, col)]
                print(t.id, end=" ")
            print()
        locs = (
            (0, 0),
            (0, square_size - 1),
            (square_size - 1, square_size - 1),
            (square_size - 1, 0)
        )
        value = functools.reduce(lambda a, b: a * b, tuple(locations[loc][0].id for loc in locs))
        postprocess(locations)
        print(value)
        exit()
    for vec in POSITIONS:
        next_pos = move_position(position, vec)
        if next_pos in locations:
            continue
        if not is_valid_position(next_pos):
            continue
        for (next_tile, next_variant) in VALID_AT[next_pos]:
            if next_tile not in remaining:
                continue
            if match_edges(tile, next_tile, variant, next_variant, vec, OPPOSITE[vec]):
                remaining.remove(next_tile)
                locations[next_pos] = (next_tile, next_variant)
                find((next_tile, next_variant), next_pos, locations, remaining)
                del locations[next_pos]
                remaining.add(next_tile)


print("Initial LR: ", len(left_right_initial))
for (tile, variant) in left_right_initial:
    find((tile, variant), (0, 0), {(0, 0): (tile, variant)}, set(tiles) - {tile})

"""
3779 3541 2551 1297 2843 1657 3041 3371 3631 2221 1783 3061 
2521 3833 3701 2161 3461 1097 1709 2539 1987 3109 3467 2897 
2239 1489 2141 2593 1621 3613 1307 3049 1117 2963 1327 1217 
1093 2179 3331 2137 2837 2689 2389 1277 2953 1103 3943 1979 
3547 1583 1423 1249 2459 1361 1697 2053 3559 3347 3203 2003 
1777 2207 3359 1163 3727 1223 1571 2713 1811 1907 3491 3067 
2441 2143 1031 3083 3433 2081 1567 3463 3593 2909 3529 1237 
3191 3793 3313 3413 2131 1069 2731 3121 1259 1439 2861 3389 
2857 1867 2633 3923 1433 2063 3407 3557 1523 1009 1559 2647 
1889 2927 1231 3607 3929 1283 3449 3947 2579 2153 2287 1597 
1289 3001 1171 3319 1493 1753 3253 2693 2089 3169 3673 3761 
3329 3853 2503 2351 1453 1931 2039 1667 1747 2591 1187 2789 
107399567124539
"""
