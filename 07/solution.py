from collections import defaultdict
# striped olive bags contain 4 dark crimson bags.
adj = defaultdict(list)
keys = []

def parse_line(line):
    toks = line.split()
    curr = []
    bag = None
    j = 0
    for i in range(len(toks)):
        if toks[i] == "bags":
            bag = " ".join(curr)
            keys.append(bag)
            curr.clear()
        elif toks[i] == "contain":
            j = i+1
            break
        else:
            curr.append(toks[i])
    rest = toks[j:]
    if "no other" in rest:
        adj[bag] = []
        return
    curr = []
    print(rest)
    for word in rest:
        if "bag" in word:
            b = " ".join(curr)
            adj[bag].append(b)
            curr.clear()
        elif not word.isalpha():
            continue
        else:
            curr.append(word)
    if len(curr) != 0:
        b = " ".join(curr)
        adj[bag].append(b)

with open('test_input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

count = 0

def dfs(bag):
    global count
    visited = set()
    s = []
    s.append(bag)
    while len(s) != 0:
        b = s.pop()
        visited.add(b)
        for c in adj[b]:
            if c not in visited:
                if c == "shiny gold":
                    count += 1
                s.append(c)

for bag in keys:
    dfs(bag)

print(count)
