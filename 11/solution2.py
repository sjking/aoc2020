from collections import defaultdict

seats = []

def parse_line(line):
    row = list(line)
    seats.append(row)

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

rows, cols = len(seats), len(seats[0])

def occupied(i, j):
    num_occupied = 0
    for x, y in [(-1 ,-1), (-1, 0), (-1, +1), (0, +1), (+1, +1),
                 (+1, 0), (+1, -1), (0, -1)]:
        a, b = x + i, y + j
        while a >= 0 and a < rows and b >= 0 and b < cols:
            if seats[a][b] == "#":
                num_occupied += 1
                break
            elif seats[a][b] == "L":
                break
            a += x
            b += y
    return num_occupied

def flip(i, j):
    if seats[i][j] == "L":
        seats[i][j] = "#"
    elif seats[i][j] == "#":
        seats[i][j] = "L"

def round():
    s = []
    for i in range(rows):
        for j in range(cols):
            seat = seats[i][j]
            if seat == ".":
                continue
            num_occupied = occupied(i, j)
            if seat == "L" and num_occupied == 0:
                s.append((i, j))
            elif seat == "#" and num_occupied >= 5:
                s.append((i, j))
    if len(s) == 0:
        return False
    for x, y in s:
        flip(x, y)
    return True

while round():
    pass

occupied = 0
for i in range(len(seats)):
        for j in range(len(seats[0])):
            if seats[i][j] == "#":
                occupied += 1

print(occupied)
