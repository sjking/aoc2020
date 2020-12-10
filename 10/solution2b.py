from collections import defaultdict

jolts = []

def parse_line(line):
    jolts.append(int(line))

with open('test_input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

jolts.sort()
n = len(jolts)
ways = 0
memo = dict()

def perms(i, prev):
    if (i, prev) in memo:
        return memo[(i, prev)]
    if i == n:
        if jolts[i-1] + 3 - prev <= 3:
            return 1
        return 0
    d = jolts[i] - prev
    if d <= 3:
        memo[(i, prev)] = perms(i+1, jolts[i]) + perms(i+1, prev)
        return memo[(i, prev)]
    return 0

perms(0, 0)
print(memo[(0,0)])
