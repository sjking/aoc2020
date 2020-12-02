s, l = set(), list()

with open('input', 'r') as f:
    for line in f:
        num = int(line.rstrip())
        s.add(num)
        l.append(num)

found = False

for num in l:
    if 2020 - num in s:
        print(num * (2020 - num))
        found = True
        break

if not found:
    print("no dice")
