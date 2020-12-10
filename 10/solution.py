from collections import defaultdict

jolts = []

def parse_line(line):
    jolts.append(int(line))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

jolts.sort()

d = defaultdict(int)

i = 0
d[jolts[0]] = jolts[0]
while i < len(jolts) - 1:
    d[jolts[i+1] - jolts[i]] += 1
    i += 1
d[3] += 1
print(d)
