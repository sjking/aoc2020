import sys
import os
import time
from dataclasses import dataclass
from collections import defaultdict

sys.setrecursionlimit(1000)
IN_FIlE = "input"
PATH = os.path.dirname(os.path.realpath(__file__))

directions = {"e", "se", "sw", "w", "nw", "ne"}


@dataclass
class Position:
    e: int = 0
    w: int = 0
    se: int = 0
    nw: int = 0
    sw: int = 0
    ne: int = 0

    def key(self):
        return self.e, self.w, self.se, self.nw, self.sw, self.ne


def update_position(position, tile):
    if tile == "e":
        position.e += 1
    elif tile == "w":
        position.w += 1
    elif tile == "se":
        position.se += 1
    elif tile == "nw":
        position.nw += 1
    elif tile == "sw":
        position.sw += 1
    elif tile == "ne":
        position.ne += 1


def simplify(pos):
    def simplify_prime():
        e, w = pos.e, pos.w
        pos.e = max(0, e - w)
        pos.w = max(0, w - e)
        se, nw = pos.se, pos.nw
        pos.se = max(0, se - nw)
        pos.nw = max(0, nw - se)
        sw, ne = pos.sw, pos.ne
        pos.sw = max(0, sw - ne)
        pos.ne = max(0, ne - sw)

        # se/ne
        ne, se = pos.ne, pos.se
        pos.e += min(ne, se)
        pos.ne = max(0, ne - se)
        pos.se = max(0, se - ne)
        # e/sw
        e, sw = pos.e, pos.sw
        pos.se += min(e, sw)
        pos.e = max(0, e - sw)
        pos.sw = max(0, sw - e)
        # w/se
        w, se = pos.w, pos.se
        pos.sw += min(w, se)
        pos.w = max(0, w - se)
        pos.se = max(0, se - w)
        # nw/sw
        nw, sw = pos.nw, pos.sw
        pos.w += min(nw, sw)
        pos.nw = max(0, nw - sw)
        pos.sw = max(0, sw - nw)
        # w/ne
        w, ne = pos.w, pos.ne
        pos.nw += min(w, ne)
        pos.w = max(0, w - ne)
        pos.ne = max(0, ne - w)
        # nw/e
        nw, e = pos.nw, pos.e
        pos.ne += min(nw, e)
        pos.nw = max(0, nw - e)
        pos.e = max(0, e - nw)

    key = pos.key()
    while True:
        simplify_prime()
        new_key = pos.key()
        if new_key == key:
            break
        key = new_key


def solution_1(tiles):
    positions = dict()
    for tile in tiles:
        i = 0
        n = len(tile)
        curr_position = Position()
        while i < n - 1:
            if tile[i:i+2] in directions:
                direction = tile[i:i+2]
                i += 2
            else:
                direction = tile[i]
                i += 1
            update_position(curr_position, direction)
        if i == len(tile) - 1:
            update_position(curr_position, tile[i])
        simplify(curr_position)
        key = curr_position.key()
        if key in positions:
            positions[key] = not positions[key]
        else:
            positions[key] = False
    num_black = 0
    for color in positions.values():
        if not color:
            num_black += 1
    return num_black


def solution_2():
    pass


def parse_line(line, tiles):
    tiles.append(line)


def main(infile=IN_FIlE, path=PATH):
    input_file = f"{path}/resources/{infile}"
    tiles = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parse_line(line, tiles)
    start = time.monotonic()
    result_1 = solution_1(tiles)
    result_2 = solution_2()
    end = time.monotonic()
    print(f"Elapsed time: {end - start} seconds")
    print(f"Part 1: {result_1}")
    print(f"Part 2: {result_2}")


if __name__ == '__main__':
    main()
