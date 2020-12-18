from collections import defaultdict

commands = []

def parse_line(line):
    cmd, v = line.split("=")
    if "mask" in cmd:
        commands.append(("mask", (v.strip())))
    else:
        cmd.strip()
        rest = cmd[4:]
        rest = rest.split("]")
        address = int(rest[0])
        commands.append((address, int(v.strip())))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

mem = defaultdict(str)
mask = ""


def to_bin(num):
    b = []
    while num > 0:
        b.append(str(num % 2))
        num //= 2
    while len(b) < 36:
        b.append("0")
    s = "".join(reversed(b))
    return s

def to_int(b):
    p = 0
    i = len(b) - 1
    n = 0
    while i >= 0:
        n += (2 ** p) * int(b[i])
        i -= 1
        p += 1
    return n

mask = ""
for x, y in commands:
    if x == "mask":
        mask = y
    else:
        address, val = x, y
        val = to_bin(val)
        new_val = list(to_bin(0))
        for i in range(36):
            if mask[i] == "X":
                new_val[i] = val[i]
            else:
                new_val[i] = mask[i]
        mem[address] = "".join(new_val)

s = 0
for b in mem.values():
    s += to_int(b)
print(s)
