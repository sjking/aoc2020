from collections import defaultdict

jolts = []

def parse_line(line):
    jolts.append(int(line))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

jolts.sort()
n = len(jolts)
ways = 0

def perms(i, prev):
    global ways
    if i == n:
        if jolts[i-1] + 3 - prev <= 3:
            ways += 1
        return
    d = jolts[i] - prev
    if d <= 3:
        perms(i+1, jolts[i])
        perms(i+1, prev)

perms(0, 0)
print(ways)
