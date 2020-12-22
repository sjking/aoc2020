import sys
import os
import time
from dataclasses import dataclass

sys.setrecursionlimit(1000)
IN_FIlE = "input"
PATH = os.path.dirname(os.path.realpath(__file__))


@dataclass()
class Trie:
    terminal: bool
    table: dict


def parse_line(line, section, rules, messages):
    if section == 0:
        _, y = line.split(":")
        z = y.split("|")
        rs = []
        for x in z:
            ys = []
            for y in x.split():
                if '"' in y:
                    ys.append(y[1:2])
                else:
                    ys.append(y)
            rs.append(ys)
        rules.append(rs)
    else:
        messages.append(line)


def build_trie(messages):
    trie = Trie(terminal=False, table=dict())
    for message in messages:
        n = len(message)
        t = trie
        for i, c in enumerate(message):
            if c in t.table:
                t = t.table[c]
            else:
                t.table[c] = Trie(terminal=(i == n - 1), table=dict())
                t = t.table[c]
    return trie


def search(c, tries, rules):
    if c.isalpha():
        return [trie.table[c] for trie in tries if c in trie.table]
    nodes = []
    for group in rules[int(c)]:
        curr_tries = tries
        for i, k in enumerate(group):
            ts = search(k, curr_tries, rules)
            ts_prime = []
            for t in ts:
                if not t.terminal:
                    ts_prime.append(t)
                elif i == len(group) - 1:
                    ts_prime.append(t)
            curr_tries = ts_prime
        nodes.extend(curr_tries)
    return nodes


def display(num_valid):
    print(f"number valid: {num_valid}")


def main(infile=IN_FIlE, path=PATH):
    rules = []
    messages = []

    input_file = f"{path}/resources/{infile}"
    with open(input_file, 'r') as f:
        section = 0
        for line in f:
            line = line.strip()
            if not line:
                section = 1
                continue
            parse_line(line, section, rules, messages)
    trie = build_trie(messages)
    start = time.monotonic()
    tries = search("0", [trie], rules)
    end = time.monotonic()
    print(f"Total time: {end - start} seconds")
    num_valid = len(list(filter(lambda t: t.terminal, tries)))
    display(num_valid)


if __name__ == '__main__':
    main()