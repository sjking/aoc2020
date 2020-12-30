import sys
import os
import time
from dataclasses import dataclass

sys.setrecursionlimit(1000)
IN_FIlE = "input"
PATH = os.path.dirname(os.path.realpath(__file__))


class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None


def parse_line(line):
    return list(map(int, list(line)))


def build_linked_list(nums):
    head = Node(nums[0])
    curr = head
    for i in range(1, len(nums)):
        node = Node(nums[i])
        curr.right = node
        node.left = curr
        curr = node
    curr.right = head
    head.left = curr
    return head


def build_dictionary(L):
    d = dict()
    curr = L
    while curr.value not in d:
        d[curr.value] = curr
        curr = curr.right
    return d


def solution(nums):
    curr = build_linked_list(nums)
    d = build_dictionary(curr)
    for round in range(100):
        a, b, c = curr.right, curr.right.right, curr.right.right.right
        s = {a.value, b.value, c.value}
        curr.right = c.right
        curr.right.left = curr
        dest = curr.value - 1
        if dest == 0:
            dest = 9
        while dest in s:
            if dest == 1:
                dest = 9
            else:
                dest -= 1
        dc = d[dest]
        a.left = dc
        c.right = dc.right
        dc.right.left = c
        dc.right = a
        curr = curr.right
    curr = d[1].right
    result = []
    while len(result) < 8:
        result.append(curr.value)
        curr = curr.right
    return result


def solution_2(nums):
    for i in range(10, 1_000_001):
        nums.append(i)
    curr = build_linked_list(nums)
    d = build_dictionary(curr)
    for round in range(10_000_000):
        if round % 1_000_000 == 0:
            print(f"{10_000_000 - round} to go...")
        a, b, c = curr.right, curr.right.right, curr.right.right.right
        s = {a.value, b.value, c.value}
        curr.right = c.right
        curr.right.left = curr
        dest = curr.value - 1
        if dest == 0:
            dest = 1_000_000
        while dest in s:
            if dest == 1:
                dest = 1_000_000
            else:
                dest -= 1
        dc = d[dest]
        a.left = dc
        c.right = dc.right
        dc.right.left = c
        dc.right = a
        curr = curr.right
    a, b = d[1].right, d[1].right.right
    return a.value * b.value


def main(infile=IN_FIlE, path=PATH):
    input_file = f"{path}/resources/{infile}"
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            nums = parse_line(line)
    start = time.monotonic()
    result_1 = solution(nums)
    result_2 = solution_2(nums)
    end = time.monotonic()
    print(f"Part 1: {''.join(map(str, result_1))}")
    print(f"Part 2: {result_2}")
    print(f"Time: {end - start} seconds")


if __name__ == '__main__':
    main()