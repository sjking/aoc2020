numbers = []
window = []
s = set()
x = 25

def parse_line(line):
    numbers.append(int(line))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        parse_line(line)

for i in range(x):
    s.add(numbers[i])
    window.append(numbers[i])

j = x
k = 0
num = 0
while True:
    num = numbers[j]
    found = False
    for a in window:
        b = num - a
        if b != a and b in s:
            s.remove(window[k % x])
            s.add(num)
            window[k % x] = num
            k += 1
            j += 1
            found = True
            break
    if not found:
        break

print(num)

lo, hi, s = 0, 0, numbers[0]

# Note: This does not generalize, but works for my input
while hi < j and s != num:
    while s < num and hi < j:
        hi += 1
        s += numbers[hi]
    if s == num:
        break
    while s > num and lo < hi:
        s -= numbers[lo]
        lo += 1
    if s == num:
        break

if s == num:
    print(min(numbers[lo:hi+1]) + max(numbers[lo:hi+1]))

