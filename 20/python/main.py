from dataclasses import dataclass, field
from typing import List
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
        return
    if "Tile" in line:
        curr_tiles.clear()
        toks = line.split()
        tile_id = int(toks[1][:-1])
        for r in range(4):
            tile = Tile(num=tile_id)
            tile_info = TileInfo(tile=tile, rotation=r)
            curr_tiles.append(tile_info)
        return
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
                tile_infos.append(tile_info)
            elif r == 1:
                t.n, t.e, t.s, t.w = rev(w), n, rev(e), s
            elif r == 2:
                t.n, t.e, t.s, t.w = rev(s), rev(w), rev(n), rev(e)
            elif r == 3:
                t.n, t.e, t.s, t.w = e, rev(s), w, rev(n)
            tile_infos.append(tile_info)


def main(input_file):
    curr_tiles = []
    tile_infos = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            parse_line(line, tile_infos, curr_tiles)
    print("w")


if __name__ == '__main__':
    infile = "test_input_sm"
    path = os.path.dirname(os.path.realpath(__file__))
    main(f"{path}/resources/{infile}")
