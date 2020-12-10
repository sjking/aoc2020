instructions = []

def parse_line(line):
    cmd, val = line.split()
    val = int(val)
    instructions.append((cmd, val))

with open('test_input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

visited = set()
i = 0
while i not in visited:
    visited.add(i)
    cmd, val = instructions[i]
    if cmd == "acc":
        i += 1
    elif cmd == "jmp":
        i += val
    elif cmd == "nop":
        i += 1

path = list(visited)

def check_path(k):
    ins = instructions.copy()
    cmd, val = ins[k]
    if cmd == "jmp":
        ins[k] = ("nop", val)
    else:
        ins[k] = ("jmp", val)
    visited = set()
    j = 0
    acc = 0
    while j not in visited and j != len(ins):
        visited.add(j)
        cmd, val = ins[j]
        if cmd == "acc":
            acc += val
            j += 1
        elif cmd == "jmp":
            j += val
        elif cmd == "nop":
            j += 1
    if j == len(ins):
        return True, acc
    else:
        return False, 0


for j in path:
    if instructions[j][0] == "jmp" or instructions[j][0] == "nop":
        is_valid, acc = check_path(j)
        if is_valid:
            print(acc)
            break


