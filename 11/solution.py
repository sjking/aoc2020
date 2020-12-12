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

def adjacent(i, j):
    adj = {"L":0, "#":0, ".":0}
    for x, y in [(i-1 ,j-1), (i-1, j), (i-1, j+1), (i, j+1), (i+1, j+1),
                 (i+1, j), (i+1, j-1), (i, j-1)]:
        if x >= 0 and x < rows and y >= 0 and y < cols:
            adj[seats[x][y]] += 1
    return adj

def flip(i, j):
    if seats[i][j] == "L":
        seats[i][j] = "#"
    elif seats[i][j] == "#":
        seats[i][j] = "L"

def round():
    s = []
    for i in range(len(seats)):
        for j in range(len(seats[0])):
            seat = seats[i][j]
            adj = adjacent(i, j)
            if seat == "L" and adj["#"] == 0:
                s.append((i, j))
            elif seat == "#" and adj["#"] >= 4:
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
