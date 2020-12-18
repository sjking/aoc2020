fields = dict()
section = "A"
your_ticket = []
nearby_tickets = []

def parse_line(line):
    global your_ticket, nearby_tickets, section
    if section == "A":
        toks = line.split(":")
        field = toks[0].strip()
        rest = toks[1].strip().split()
        a, b = rest[0].split("-")
        c, d = rest[2].split("-")
        fields[field] = ((int(a), int(b)), (int(c), int(d)))
    elif section == "B":
        your_ticket = list(map(int, line.split(",")))
    elif section == "C":
        nearby_tickets.append(list(map(int, line.split(","))))

with open('test_input', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        elif "your ticket" in line:
            section = "B"
            continue
        elif "nearby tickets" in line:
            section = "C"
            continue
        else:
            parse_line(line)

def insert_range(tup, ranges):
    if not ranges:
        ranges.append(tup)
        return
    new_a, new_b = tup
    curr_a, curr_b = ranges[0]
    i = 1
    while i < len(ranges) and new_a > curr_b:
        curr_a, curr_b = ranges[i]
        i += 1
    if new_a == curr_b + 1:
        ranges[i-1] = (curr_a, new_b)
    elif new_a > curr_b:
        ranges.append(tup)
    elif new_b >= curr_a:
        j = i
        while j < len(ranges) and new_b > curr_b:
            curr_a, curr_b = ranges[j]
            j += 1
        ranges[i-1] = (min(new_a, curr_a), max(new_b, curr_b))
        # all ranges[i:j] are deleted
        k, l = i, j
        while l < len(ranges):
            ranges[k] = ranges[l]
            k += 1
            l += 1
        for _ in range(i, j):
            ranges.pop()

valid_ranges = []
for r in fields.values():
    a, b = r
    insert_range(a, valid_ranges)
    insert_range(b, valid_ranges)

def test():
    t = []
    for tup in [(1,3), (4,7), (6, 12), (23, 45)]:
        insert_range(tup, t)
    assert t == [(1, 12), (23, 45)]
    t = []
    for tup in [(9,13), (4,7), (2, 12), (13, 45)]:
        insert_range(tup, t)
    assert t == [(2, 45)]

def in_range(n, ranges):
    for lo, hi in ranges:
        if lo <= n <= hi:
            return True
    return False

invalid_values = []
for n in your_ticket:
    if not in_range(n, valid_ranges):
        invalid_values.append(n)
for t in nearby_tickets:
    for n in t:
        if not in_range(n, valid_ranges):
            invalid_values.append(n)
print(sum(invalid_values))
