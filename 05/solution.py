
def decode_pass(code):
    lo, hi = 0, 127
    for i in range(0, 7):
        mid = (lo + hi) // 2
        if code[i] == "F":
            hi = mid
        else:
            lo = mid + 1
    row = hi
    lo, hi = 0, 7
    for j in range(7, 10):
        mid = (lo + hi) // 2
        if code[j] == "L":
            hi = mid
        else:
            lo = mid + 1
    col = hi
    return row * 8 + col

maximum = 0

seats = []

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        sid = decode_pass(line)
        maximum = max(sid, maximum)
        seats.append(sid)

seats.sort()
for i in range(len(seats)-1):
    if seats[i] + 2 == seats[i+1]:
        print(seats[i] + 1)


print(maximum)
