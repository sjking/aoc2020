import sys
import os
import time
from dataclasses import dataclass

sys.setrecursionlimit(1000)
IN_FIlE = "input"
PATH = os.path.dirname(os.path.realpath(__file__))


def find_loop_size(pub):
    loop = 0
    val = 1
    subject_number = 7
    while val != pub:
        loop += 1
        val *= subject_number
        val = val % 20201227
    return loop


def transform(subject_number, loop_size):
    val = 1
    for _ in range(loop_size):
        val *= subject_number
        val = val % 20201227
    return val


def solution_1(card, door):
    card_loop_size = find_loop_size(card)
    door_loop_size = find_loop_size(door)
    print(f"Card loop size: {card_loop_size}")
    print(f"Door loop size: {door_loop_size}")
    card_key = transform(door, card_loop_size)
    print(f"Card key: {card_key}")
    door_key = transform(card, door_loop_size)
    print(f"Card key: {door_key}")
    assert card_key == door_key


def solution_2(x):
    pass


def parse_line(line, numbers):
    numbers.append(line)


def main(infile=IN_FIlE, path=PATH):
    input_file = f"{path}/resources/{infile}"
    numbers = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parse_line(line, numbers)
    card, door = int(numbers[0]), int(numbers[1])
    start = time.monotonic()
    result_1 = solution_1(card, door)
    # result_2 = solution_2(tiles)
    end = time.monotonic()
    print(f"Elapsed time: {end - start} seconds")
    print(f"Part 1: {result_1}")
    # print(f"Part 2: {result_2}")


if __name__ == '__main__':
    main()
