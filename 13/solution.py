from collections import defaultdict

depart = None
buses = None

def parse_bus(line):
    return list(map(int, filter(lambda x: x != 'x', line.split(","))))

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        if depart is None:
            depart = int(line)
        else:
            buses = parse_bus(line)
            break

def find_time(bus_id):
    global depart
    if depart % bus_id == 0:
        return depart
    return (depart // bus_id) * bus_id + bus_id

d, b_id = min(zip(list(map(find_time, buses)), buses))
print((d - depart) * b_id)

