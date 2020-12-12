from collections import defaultdict

moves = []

def parse_line(line):
    d, v = line[0], line[1:]
    moves.append((d, int(v)))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

pos = (0, 0)
direction = 0

def handle_move(d, v, pos):
    x, y = pos
    if d == 0:
        x += v
    elif d == 90:
        y += v
    elif d == 270:
        y -= v
    elif d == 180:
        x -= v
    return (x, y)

for d, v in moves:
    print(pos)
    if d == "F":
        pos = handle_move(direction, v, pos)
    elif d == "L":
        direction = (direction + v) % 360
    elif d == "R":
        direction = (direction - v) % 360
    elif d == "E":
        pos = handle_move(0, v, pos)
    elif d == "N":
        pos = handle_move(90, v, pos)
    elif d == "W":
        pos = handle_move(180, v, pos)
    elif d == "S":
        pos = handle_move(270, v, pos)


print(moves)
print(abs(pos[0]) + abs(pos[1]))
