from dataclasses import dataclass, field
from collections import defaultdict
import time
from typing import List
from math import sqrt
import os


@dataclass
class Tile:
    num: int
    n: List[str] = field(default_factory=list)
    e: List[str] = field(default_factory=list)
    s: List[str] = field(default_factory=list)
    w: List[str] = field(default_factory=list)


@dataclass(order=True)
class TileInfo:
    tile: Tile
    rotation: int = 0
    flipped: bool = False


def rev(ls):
    return list(reversed(ls))


def flipped_v(tile_info):
    tile = tile_info.tile
    new_tile = Tile(num=tile.num, n=tile.s, e=rev(tile.e), s=tile.n, w=rev(tile.w))
    new_tile_info = TileInfo(tile=new_tile,
                             rotation=tile_info.rotation,
                             flipped=True)
    return new_tile_info


def flipped_h(tile_info):
    tile = tile_info.tile
    new_tile = Tile(num=tile.num, n=rev(tile.n), e=tile.w, s=rev(tile.s), w=tile.e)
    new_tile_info = TileInfo(tile=new_tile,
                             rotation=tile_info.rotation,
                             flipped=True)
    return new_tile_info


def parse_line(line, tile_infos, curr_tiles):
    if not line:
        return 0
    if "Tile" in line:
        curr_tiles.clear()
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
    tile.w.append(line[0])
    tile.e.append(line[-1])
    if len(tile.e) == n:
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

    n = 0
    for tile_info in tile_infos:
        n += 1
        print(f"Trying starting from tile {n}")
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


def main(input_file):
    curr_tiles = []
    tile_infos = []
    num_tiles = 0
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            num_tiles += parse_line(line, tile_infos, curr_tiles)
    table, counts = build_table(tile_infos)
    sz = round(sqrt(num_tiles))
    grid = [[None for _ in range(sz)] for _ in range(sz)]
    start = time.monotonic()
    build_grid(table, grid, sz, tile_infos, counts)
    answer_part_1 = calculate_answer_1(grid, sz)
    end = time.monotonic()
    print(f"Total Time: {end - start} seconds")
    print(f"Part 1: {answer_part_1}")


if __name__ == '__main__':
    infile = "input"
    path = os.path.dirname(os.path.realpath(__file__))
    main(f"{path}/resources/{infile}")
