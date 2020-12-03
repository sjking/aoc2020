m = []

with open('input', 'r') as f:
    for line in f:
        m.append(list(line.rstrip()))

rows = len(m)
cols = len(m[0])


def go(r, d):
    num_trees = 0
    i, j = 0, 0
    while i < rows:
        if m[i][j % cols] == '#':
            num_trees += 1
        i += d
        j += r
    return num_trees

total = 1

for r, d in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
    result = go(r, d)
    total = total * result

print(total)


"""

    Right 1, down 1.
    Right 3, down 1. (This is the slope you already checked.)
    Right 5, down 1.
    Right 7, down 1.
    Right 1, down 2.
"""

