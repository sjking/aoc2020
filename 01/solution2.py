from collections import defaultdict

d, l = defaultdict(set), list()

i = 0
with open('input', 'r') as f:
    for line in f:
        num = int(line.rstrip())
        l.append(num)
        d[num].add(i)

n = len(l)

for i in range(n):
    for j in range(i + 1, n):
        k = 2020 - (l[i] + l[j])
        if k in d and len(d[k] - {i, j}) != 0:
            print(f"{l[i]} * {l[j]} * {k} = {l[i] * l[j] * k}")



