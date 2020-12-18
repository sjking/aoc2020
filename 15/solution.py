from collections import defaultdict

start_numbers = []
def parse_line(line):
    start_numbers = list(map(int, line.split(",")))
    return start_numbers


with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        start_numbers = parse_line(line)
        break

print(start_numbers)
t = 0
nums = dict()
for n in start_numbers[:-1]:
    t += 1
    nums[n] = t

prev = start_numbers[-1]
t += 1
prevs = []
prevs.append(prev)
print(prev, t)
print(nums)
while t < 2020:
    if prev in nums:
        tmp = nums[prev]
        nums[prev] = t
        prev = t - tmp
    else:
        nums[prev] = t
        prev = 0
    prevs.append(prev)
    t += 1

print(prev)
