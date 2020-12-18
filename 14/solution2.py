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

def to_bin(num):
    b = []
    while num > 0:
        b.append(str(num % 2))
        num //= 2
    while len(b) < 36:
        b.append("0")
    s = "".join(reversed(b))
    return s

def get_addresses(b, i, p, acc, addresses):
    if i == -1:
        return addresses.append(acc)
    if b[i] == "X":
        get_addresses(b, i-1, p+1, acc + 2**p, addresses)
        get_addresses(b, i-1, p+1, acc, addresses)
    else:
        get_addresses(b, i-1, p+1, acc + int(b[i]) * 2**p, addresses)

mask = ""
mem = defaultdict(int)
for x, y in commands:
    if x == "mask":
        mask = y
    else:
        address, val = x, y
        new_address = list(to_bin(address))
        for i in range(36):
            if mask[i] == "X":
                new_address[i] = "X"
            elif mask[i] == "1":
                new_address[i] = "1"
            else:
                new_address[i] = new_address[i]
        addresses = []
        get_addresses(new_address, 35, 0, 0, addresses)
        for address in addresses:
            mem[address] = val

print(sum(mem.values()))
