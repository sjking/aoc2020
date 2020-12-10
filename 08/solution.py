instructions = []

def parse_line(line):
    cmd, val = line.split()
    val = int(val)
    instructions.append((cmd, val))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

visited = set()
acc = 0
i = 0
while i not in visited:
    visited.add(i)
    cmd, val = instructions[i]
    if cmd == "acc":
        acc += val
        i += 1
    elif cmd == "jmp":
        i += val
    elif cmd == "nop":
        i += 1

print(acc)

