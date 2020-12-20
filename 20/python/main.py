from dataclasses import dataclass, field
from collections import defaultdict
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


@dataclass
class TileInfo:
    tile: Tile
    rotation: int = 0


def rev(ls):
    return list(reversed(ls))


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
    return 0


def make_key(ls):
    return "".join(ls)


def build_table(tile_infos):
    table = {"n": defaultdict(list),
             "e": defaultdict(list),
             "s": defaultdict(list),
             "w": defaultdict(list)}
    for tile_info in tile_infos:
        t = tile_info.tile
        n, e, s, w = make_key(t.n), make_key(t.e), make_key(t.s), make_key(t.w)
        ns, es, ss, ws = table["n"][n], table["e"][e], table["s"][s], table["w"][w]
        if tile_info not in ns:
            ns.append(tile_info)
        if tile_info not in es:
            es.append(tile_info)
        if tile_info not in ss:
            ss.append(tile_info)
        if tile_info not in ws:
            ws.append(tile_info)
    return table


def print_solution(grid, sz):
    t1, t2, t3, t4 = grid[0][0], grid[0][sz - 1], grid[sz - 1][0], grid[sz - 1][sz - 1]
    p = 1
    for t in [t1, t2, t3, t4]:
        p *= t.tile.num
    print(p)


def build_grid(table, grid, sz, tile_infos):
    used = set()
    solution = [None]

    def search(pos):
        print(pos)
        if pos == sz * sz:
            solution[0] = grid.copy()
            return
        row, col = pos // sz, pos % sz
        left_tile = None if col == 0 else grid[row][col - 1]
        above_tile = None if row == 0 else grid[row - 1][col]
        if not above_tile:
            for t in table["w"][make_key(left_tile.tile.e)]:
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
                if t.tile.num not in used:
                    used.add(t.tile.num)
                    grid[row][col] = t
                    search(pos + 1)
                    if solution[0]:
                        return
                    grid[row][col] = None
                    used.remove(t.tile.num)
        else:
            for t in table["w"][make_key(left_tile.tile.e)]:
                for u in table["n"][make_key(above_tile.tile.s)]:
                    if t == u and u.tile.num not in used:
                        used.add(t.tile.num)
                        grid[row][col] = t
                        search(pos + 1)
                        if solution[0]:
                            return
                        grid[row][col] = None
                        used.remove(t.tile.num)

    for tile_info in tile_infos:
        tile = tile_info.tile
        grid[0][0] = tile_info
        used.add(tile.num)
        search(1)
        if solution[0]:
            print_solution(grid, sz)
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
    table = build_table(tile_infos)
    sz = round(sqrt(num_tiles))
    grid = [[None for _ in range(sz)] for _ in range(sz)]
    build_grid(table, grid, sz, tile_infos)


if __name__ == '__main__':
    infile = "test_input"
    path = os.path.dirname(os.path.realpath(__file__))
    main(f"{path}/resources/{infile}")
