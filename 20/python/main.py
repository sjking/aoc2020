from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
import time
from typing import List
from math import sqrt
import os


MONSTER = ["                  # ",
           "#    ##    ##    ###",
           " #  #  #  #  #  #   "]


@dataclass
class Tile:
    num: int
    n: List[str] = field(default_factory=list)
    e: List[str] = field(default_factory=list)
    s: List[str] = field(default_factory=list)
    w: List[str] = field(default_factory=list)


class Flip(Enum):
    none = "none"
    horizontal = "horizontal"
    vertical = "vertical"


@dataclass(order=True)
class TileInfo:
    tile: Tile
    rotation: int = 0
    flipped: Flip = Flip.none


def rev(ls):
    return list(reversed(ls))


def flipped_v(tile_info):
    tile = tile_info.tile
    new_tile = Tile(num=tile.num, n=tile.s, e=rev(tile.e), s=tile.n, w=rev(tile.w))
    new_tile_info = TileInfo(tile=new_tile,
                             rotation=tile_info.rotation,
                             flipped=Flip.vertical)
    return new_tile_info


def flipped_h(tile_info):
    tile = tile_info.tile
    new_tile = Tile(num=tile.num, n=rev(tile.n), e=tile.w, s=rev(tile.s), w=tile.e)
    new_tile_info = TileInfo(tile=new_tile,
                             rotation=tile_info.rotation,
                             flipped=Flip.horizontal)
    return new_tile_info


def parse_line(line, tile_infos, curr_tiles, raw_tiles, curr_lines):
    if not line:
        return 0
    if "Tile" in line:
        curr_tiles.clear()
        curr_lines.clear()
        toks = line.split()
        tile_id = int(toks[1][:-1])
        for r in range(4):
            tile = Tile(num=tile_id)
            tile_info = TileInfo(tile=tile, rotation=r)
            curr_tiles.append(tile_info)
        return 1
    tile = curr_tiles[0].tile
    if not tile.n:
        tile.n = list(line)
    n = len(tile.n)
    curr_lines.append(line)
    tile.w.append(line[0])
    tile.e.append(line[-1])
    if len(tile.e) == n:
        raw_tiles[tile.num] = list(map(list, curr_lines))
        tile.s = list(line)
        n, s, e, w = tile.n, tile.s, tile.e, tile.w
        for tile_info in curr_tiles:
            r = tile_info.rotation
            t = tile_info.tile
            if r == 0:
                pass
            elif r == 1:
                t.n, t.e, t.s, t.w = rev(w), n, rev(e), s
            elif r == 2:
                t.n, t.e, t.s, t.w = rev(s), rev(w), rev(n), rev(e)
            elif r == 3:
                t.n, t.e, t.s, t.w = e, rev(s), w, rev(n)
            tile_infos.append(tile_info)
            tile_infos.append(flipped_v(tile_info))
            tile_infos.append(flipped_h(tile_info))
    return 0


def make_key(ls):
    return "".join(ls)


def make_key_2(xs, ys):
    return "".join(xs), "".join(ys)


def build_table(tile_infos):
    table = {"n": defaultdict(list),
             "e": defaultdict(list),
             "s": defaultdict(list),
             "w": defaultdict(list),
             "nw": defaultdict(list)}
    counts = defaultdict(int)
    for tile_info in tile_infos:
        t = tile_info.tile
        n, e, s, w, nw = make_key(t.n), make_key(t.e), make_key(t.s), make_key(t.w), make_key_2(t.n, t.w)
        ns, es, ss, ws, nws = table["n"][n], table["e"][e], table["s"][s], table["w"][w], table["nw"][nw]
        if tile_info not in ns:
            ns.append(tile_info)
        if tile_info not in es:
            es.append(tile_info)
        if tile_info not in ss:
            ss.append(tile_info)
        if tile_info not in ws:
            ws.append(tile_info)
        if tile_info not in nw:
            nws.append(tile_info)
        for k in [n, e, s, w]:
            counts[k] += 1
    total_values, total_keys = 0, 0
    for k, vs in table["n"].items():
        total_keys += 1
        total_values += len(vs)
    for k, vs in table["w"].items():
        total_keys += 1
        total_values += len(vs)
    print(total_values / total_keys)
    # about 3 values per key on average
    return table, counts


def calculate_answer_1(grid, sz):
    t1, t2, t3, t4 = grid[0][0], grid[0][sz - 1], grid[sz - 1][0], grid[sz - 1][sz - 1]
    p = 1
    for t in [t1, t2, t3, t4]:
        p *= t.tile.num
    return p


def build_grid(table, grid, sz, tile_infos, counts):
    used = set()
    solution = [None]
    counter = [0]

    def search(pos):
        if pos == sz * sz:
            solution[0] = grid.copy()
            return
        counter[0] += 1
        if counter[0] % 10_000_000 == 0:
            print("Iteration: ", counter[0])
        row, col = pos // sz, pos % sz
        left_tile = None if col == 0 else grid[row][col - 1]
        above_tile = None if row == 0 else grid[row - 1][col]
        if not above_tile:
            for t in table["w"][make_key(left_tile.tile.e)]:
                if counts[make_key(t.tile.n)] > 8 and counts[make_key(t.tile.w)] > 8:
                    continue
                if col == sz - 1 and counts[make_key(t.tile.e)] > 8:
                    continue
                if t.tile.num not in used:
                    used.add(t.tile.num)
                    grid[row][col] = t
                    search(pos + 1)
                    if solution[0]:
                        return
                    grid[row][col] = None
                    used.remove(t.tile.num)
        elif not left_tile:
            for t in table["n"][make_key(above_tile.tile.s)]:
                if counts[make_key(t.tile.w)] > 8:
                    continue
                if t.tile.num not in used:
                    used.add(t.tile.num)
                    grid[row][col] = t
                    search(pos + 1)
                    if solution[0]:
                        return
                    grid[row][col] = None
                    used.remove(t.tile.num)
        else:
            for t in table["nw"][make_key_2(above_tile.tile.s, left_tile.tile.e)]:
                if row == sz - 1 and counts[make_key(t.tile.s)] > 8:
                    continue
                if col == sz - 1 and counts[make_key(t.tile.e)] > 8:
                    continue
                if t.tile.num not in used:
                    used.add(t.tile.num)
                    grid[row][col] = t
                    search(pos + 1)
                    if solution[0]:
                        return
                    grid[row][col] = None
                    used.remove(t.tile.num)

    for tile_info in tile_infos:
        tile = tile_info.tile
        if counts[make_key(tile.n)] > 8 and counts[make_key(tile.w)] > 8:
            continue
        grid[0][0] = tile_info
        used.add(tile.num)
        search(1)
        if solution[0]:
            return
        used.remove(tile.num)
        grid[0][0] = None


def rotate_image(image, r):
    n = len(image)
    m = image

    def rot(l, r, t, b):
        if l < r and t < b:
            j = 0
            for i in range(l, r):
                tmp = m[t][i]
                m[t][i] = m[b - j][l]
                m[b - j][l] = m[b][r - j]
                m[b][r - j] = m[t + j][r]
                m[t + j][r] = tmp
                j += 1
            rot(l + 1, r - 1, t + 1, b - 1)

    for _ in range(r):
        rot(0, n - 1, 0, n - 1)


def flip_tile(raw_tile, flipped):
    if flipped is Flip.none:
        return
    if flipped is Flip.vertical:
        lo, hi = 0, len(raw_tile) - 1
        while lo < hi:
            tmp = raw_tile[lo]
            raw_tile[lo] = raw_tile[hi]
            raw_tile[hi] = tmp
            lo, hi = lo+1, hi-1
        return
    if flipped is Flip.horizontal:
        for row in raw_tile:
            row.reverse()
        return


def place_tile(tile_info, image, raw_tile, row, col, sz):
    raw_tile = raw_tile.copy()
    rotate_image(raw_tile, tile_info.rotation)
    flip_tile(raw_tile, tile_info.flipped)
    for i in range(1, len(raw_tile) - 1):
        for j in range(1, len(raw_tile) - 1):
            ix, jx = (row * sz) + (i - 1), (col * sz) + (j - 1)
            image[ix][jx] = raw_tile[i][j]


def search_monster(image, monster, monster_h, monster_w):
    n = len(image)
    monster_mash = False
    for row in range(n - monster_h):
        for col in range(n - monster_w):
            found = True
            for i, r in enumerate(monster):
                if not found:
                    break
                for j in r:
                    if image[row + i][col + j] != "#":
                        found = False
                        break
            if found:
                monster_mash = True
                for i, r in enumerate(monster):
                    for j in r:
                        image[row + i][col + j] = "O"
    return monster_mash


def count_rough_waters(image):
    num = 0
    for row in image:
        for c in row:
            if c == "#":
                num += 1
    return num


def copy_image(image):
    new_image = []
    for row in image:
        new_row = row.copy()
        new_image.append(new_row)
    return new_image


def find_sea_monsters(grid, raw_tiles, sz, monster):
    n = len(grid[0][0].tile.n) - 2
    m = n * sz
    image = [['.' for _ in range(m)] for _ in range(m)]
    for i, row in enumerate(grid):
        for j, tile_info in enumerate(row):
            place_tile(tile_info, image, raw_tiles[tile_info.tile.num], i, j, n)
    images = []
    for r in range(4):
        img = copy_image(image)
        rotate_image(img, r)
        images.append(img)
    flips = []
    for img in images:
        ic = copy_image(img)
        flip_tile(ic, Flip.horizontal)
        flips.append(ic)
        ic = copy_image(img)
        flip_tile(ic, Flip.vertical)
        flips.append(ic)
    images.extend(flips)
    for image in images:
        if search_monster(image, monster, len(MONSTER), len(MONSTER[0])):
            return count_rough_waters(image)
    raise Exception


def build_sea_monster(monster):
    m = []
    for line in monster:
        l = []
        for i, c in enumerate(line):
            if c == "#":
                l.append(i)
        m.append(l)
    return m


def main(input_file):
    curr_tiles = []
    tile_infos = []
    raw_tiles = dict()
    curr_lines = []
    num_tiles = 0
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            num_tiles += parse_line(line, tile_infos, curr_tiles, raw_tiles, curr_lines)
    table, counts = build_table(tile_infos)
    sz = round(sqrt(num_tiles))
    grid = [[None for _ in range(sz)] for _ in range(sz)]
    start = time.monotonic()
    build_grid(table, grid, sz, tile_infos, counts)
    answer_part_1 = calculate_answer_1(grid, sz)
    sea_monster = build_sea_monster(MONSTER)
    answer_part_2 = find_sea_monsters(grid, raw_tiles, sz, sea_monster)
    end = time.monotonic()
    print(f"Total Time: {end - start} seconds")
    print(f"Part 1: {answer_part_1}")
    print(f"Part 2: {answer_part_2}")


if __name__ == '__main__':
    infile = "input"
    path = os.path.dirname(os.path.realpath(__file__))
    main(f"{path}/resources/{infile}")
