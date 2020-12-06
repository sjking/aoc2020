

group = []

answers = []

alphabet = list("abcdefghijklmnopqrstuvwxyz")

def count_group(answers):
    if len(answers) == 0:
        return 0
    qs = set(alphabet)
    for line in answers:
        for c in line:
            if c in qs:
                qs.remove(c)
    return 26 - len(qs)

def count_group2(answers):
    if len(answers) == 0:
        return 0
    d = dict()
    for c in alphabet:
        d[c] = 0
    for line in answers:
        s = set(alphabet)
        for c in line:
            if c in s:
                d[c] += 1
                s.remove(c)
    count = 0
    for v in d.values():
        if v == len(answers):
            count += 1
    return count

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            answers.append(count_group2(group))
            group = []
        else:
            group.append(line)
    answers.append(count_group2(group))

print(sum(answers))
