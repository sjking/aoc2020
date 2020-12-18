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

with open('input', 'r') as f:
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

valid_tickets = []
for t in nearby_tickets:
    is_valid = True
    for n in t:
        if not in_range(n, valid_ranges):
            is_valid = False
            break
    if is_valid:
        valid_tickets.append(t)

your_ticket_prime = []
for n in your_ticket:
    s = set()
    for f, r in fields.items():
        (a, b), (c, d) = r
        if a <= n <= b or c <= n <= d:
            s.add(f)
    your_ticket_prime.append(s)

nearby_tickets_prime = []
for t in valid_tickets:
    ticket = []
    for n in t:
        s = set()
        for f, r in fields.items():
            (a, b), (c, d) = r
            if a <= n <= b or c <= n <= d:
                s.add(f)
        ticket.append(s)
    nearby_tickets_prime.append(ticket)

decoded = your_ticket_prime.copy()

for ticket in nearby_tickets_prime:
    decoded = list(map(lambda tup: tup[0].intersection(tup[1]), zip(decoded, ticket)))

decoded_prime = list(map(lambda tup: (len(tup[1]), tup[1], tup[0]), enumerate(decoded)))
decoded_prime.sort()

result = []
result.append((decoded_prime[0][2], decoded_prime[0][1].pop()))

for i in range(1, len(decoded_prime)):
    prev, curr = decoded_prime[i-1][1], decoded_prime[i][1]
    f = curr - prev
    f = f.pop()
    result.append((decoded_prime[i][2], f))

result.sort()
answer = 1
for v, (_, fld) in zip(your_ticket, result):
    if fld.startswith("departure"):
        answer *= v
print(answer)
