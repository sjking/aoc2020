from math import radians, cos, sin

moves = []

def parse_line(line):
    d, v = line[0], line[1:]
    moves.append((d, int(v)))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)


def rotate(waypoint, degrees):
    r = radians(degrees)
    x, y = waypoint
    x_prime = int(round(x * cos(r) - y * sin(r)))
    y_prime = int(round(x * sin(r) + y * cos(r)))
    return (x_prime, y_prime)


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

def move_ship(ship, way, v):
    xs, ys = ship
    xw, yw = way
    xs += xw * v
    ys += yw * v
    return xs, ys

def go():
    way = (10, 1)
    ship = (0, 0)
    for d, v in moves:
        if d == "F":
            ship = move_ship(ship, way, v)
        elif d == "L":
            way = rotate(way, v)
        elif d == "R":
            way = rotate(way, -v)
        elif d == "E":
            way = handle_move(0, v, way)
        elif d == "N":
            way = handle_move(90, v, way)
        elif d == "W":
            way = handle_move(180, v, way)
        elif d == "S":
            way = handle_move(270, v, way)
    return ship

ship = go()
print(abs(ship[0]) + abs(ship[1]))
