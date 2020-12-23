expressions = []

def parse_line(line):
    expressions.append(list(filter(lambda c: c != " ", line)))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

def calc(exp):
    result = int(exp[0])
    nums, ops = [], []
    nums.append(exp[0])
    i = 1
    while i < len(exp):
        if exp[i].isdigit():
            if len(ops) != 0 and ops[-1] == "+":
                nums.append(int(exp[i]) + int(nums.pop()))
                ops.pop()
            else:
                nums.append(exp[i])
        else:
            ops.append(exp[i])
        i += 1
    while len(nums) > 1:
        a = int(nums.pop())
        b = int(nums.pop())
        nums.append(a * b)
    return str(nums[0])

def evaluate(expression):
    e = expression
    s = []
    i = 0
    n = len(expression)
    while i < n:
        if e[i] == ")":
            sub = []
            while (t := s.pop()) != "(":
                sub.append(t)
            s.append(calc(list(reversed(sub))))
        else:
            s.append(e[i])
        i += 1
    return calc(s)

print(sum(map(int, map(evaluate, expressions))))
