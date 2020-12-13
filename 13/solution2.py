buses = None
depart = None

def parse_bus(line):
    buses = []
    for i, c in enumerate(line.split(",")):
        if c == "x":
            continue
        buses.append((i, int(c)))
    return buses


with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        if depart is None:
            depart = int(line)
        else:
            buses = parse_bus(line)
            break

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a % b)

# must all be coprime
for i in range(len(buses)):
    for j in range(i+1, len(buses)):
        assert gcd(buses[i][1], buses[j][1]) == 1
M = 1
for _, b in buses:
    M *= b

ms = []
for _, b in buses:
    ms.append(M // b)

# chinese remainder theorem
us = []
for i, m in enumerate(ms):
    k = 1
    while m * k % buses[i][1] != 1:
        k += 1
    us.append(k)

z = 0
for i in range(len(buses)):
    n = -buses[i][0]
    ui = us[i]
    mi = ms[i]
    z += n * ui * mi

print(z % M)
