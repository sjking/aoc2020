import math
cycles = 6

initial = []

def parse_line(line):
    initial.append(list(line))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

n = len(initial)
sz = 30
cubes = [[[['.' for _ in range(sz)] for _ in range(sz)] for _ in range(sz)] for _ in range(sz)]
margin = (sz - n) // 2
z = w = sz // 2

for i, row in enumerate(initial):
    r = margin + i
    for j, cube in enumerate(row):
        c = margin + j
        cubes[r][c][z][w] = cube

def is_active(cube):
    return cube == "#"

def num_active(i, j, k, l):
    n = 0
    for a in [-1, 0, +1]:
        for b in [-1, 0, +1]:
            for c in [-1, 0, +1]:
                for d in [-1, 0, +1]:
                    w, x, y, z = i + a, j + b, k + c, l + d
                    if 0 <= x < sz - 2 and 0 <= y < sz and 0 <= z < sz and 0 <= w < sz and is_active(cubes[w][x][y][z]):
                        n += 1
    if is_active(cubes[i][j][k][l]):
        return n - 1
    return n

def apply_actions(actions):
    for i, j, k, l in actions:
        if cubes[i][j][k][l] == "#":
            cubes[i][j][k][l] = "."
        else:
            cubes[i][j][k][l] = "#"

for cycle in range(cycles):
    actions = []
    for i in range(sz):
        for j in range(sz):
            for k in range(sz):
                for l in range(sz):
                    cube = cubes[i][j][k][l]
                    active_neighbours = num_active(i, j, k, l)
                    if is_active(cube):
                        if active_neighbours != 2 and active_neighbours != 3:
                            actions.append((i,j,k,l))
                    else:
                        if active_neighbours == 3:
                            actions.append((i,j,k,l))
    apply_actions(actions)

num_active = 0
for i in range(sz):
    for j in range(sz):
        for k in range(sz):
            for l in range(sz):
                if is_active(cubes[i][j][k][l]):
                    num_active += 1
print(num_active)



