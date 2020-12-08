import sys
sys.setrecursionlimit(1000)

from collections import defaultdict
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
    if "no" in rest and "other" in rest:
        adj[bag] = []
        return
    curr = []
    num = 0
    for word in rest:
        if "bag" in word:
            b = " ".join(curr)
            adj[bag].append((num, b))
            curr.clear()
        elif not word.isalpha():
            num = int(word)
        else:
            curr.append(word)
    if len(curr) != 0:
        b = " ".join(curr)
        adj[bag].append((num, b))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

def dfs(bag, memo):
    if bag in memo:
        return memo[bag]
    total = 1
    for n, b in adj[bag]:
        bags = dfs(b, memo)
        total += n * bags
    memo[bag] = total
    return total


memo = dict()

count = dfs("shiny gold", memo)

print(count - 1)
