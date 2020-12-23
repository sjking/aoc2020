expressions = []

def parse_line(line):
    expressions.append(list(filter(lambda c: c != " ", line)))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

def calc(exp):
    result = int(exp[0])
    i = 1
    op = ""
    while i < len(exp):
        if exp[i].isdigit():
            if op == "*":
                result *= int(exp[i])
            elif op == "+":
                result += int(exp[i])
            else:
                raise ValueError(f"Invalid operator:{op}")
        else:
            op = exp[i]
        i += 1
    return str(result)

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
