valid = 0

def is_valid(lo, hi, ch, pwd):
    cnt = 0
    for c in pwd:
        if c == ch:
            cnt += 1
    return lo <= cnt <= hi

def is_valid_2(lo, hi, ch, pwd):
    return (pwd[lo-1] == ch and pwd[hi-1] != ch) or (pwd[lo-1] != ch and pwd[hi-1] == ch)

with open('input', 'r') as f:
    for line in f:
        a, b, pswd = line.split()
        lo, hi = a.split("-")
        lo, hi = int(lo), int(hi)
        ch = b[0]
        if is_valid_2(lo, hi, ch, pswd):
            valid += 1

print(valid)
