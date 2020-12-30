from dataclasses import dataclass

@dataclass
class Tile:
    i: int
    rotation: 
    n: int = 0
    s: int = 0
    e: int = 0
    w: int = 0

tiles = []

def parse_line(line):
    if not line:
        return
    if "Tile" in line:
        toks = line.split()
        i = int(toks[1][:-1])
        tiles.append(Tile(i=i))
    tile = tiles[-1]
    if tile.n == 0:
        tile.n == len(

with open('test_input', 'r') as f:
    section = 0
    for line in f:
        line = line.strip()
        parse_line(line)

print(tiles)
