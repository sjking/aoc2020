req = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

valid = 0

curr_lines = []

"""

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

"""
def valid_field(field):
    k, v = field
    if k == "byr":
        return 1920 <= int(v) <= 2002
    elif k == "iyr":
        return 2010 <= int(v) <= 2020
    elif k == "eyr":
        return 2020 <= int(v) <= 2030
    elif k == "hgt":
        unit, num = v[-2:], int(v[:-2])
        if unit == "cm":
            return 150 <= num <= 193
        elif unit == "in":
            return 59 <= num <= 76
    elif k == "hcl":
        pound, code = v[0], v[1:]
        return pound == "#" and all(c.isalnum() for c in code)
    elif k == "ecl":
        return v in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    elif k == "pid":
        return len(v) == 9 and all(c.isdigit() for c in v)
    return False # ?

def validate_passport(lines):
    tok = set(req)
    for line in lines:
        ts = line.split()
        for t in ts:
            p = t.split(":")
            if p[0] in tok:
                if valid_field(p):
                    tok.remove(p[0])
                else:
                    return False
    return len(tok) == 0

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            if validate_passport(curr_lines):
                valid += 1
            curr_lines = []
        else:
            curr_lines.append(line)



print(valid)
