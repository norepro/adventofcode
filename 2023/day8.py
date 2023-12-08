#!/usr/bin/python3

import re
from math import lcm


def count_steps(location, turns, desert, end_condition):
    steps = 0
    while not end_condition(location):
        next = 0 if turns[steps % len(turns)] == "L" else 1
        location = desert[location][next]
        steps += 1
    return steps


with open("input.txt", "r") as f:
    turns = f.readline().strip()
    f.readline()
    desert = {}
    for line in f:
        m = re.search(r"(.+) = \((.+), (.+)\)", line)
        desert[m.group(1)] = (m.group(2), m.group(3))

part1_steps = count_steps("AAA", turns, desert, lambda x: x == "ZZZ")
print(f"Part 1: {part1_steps}")

part2_steps = [
    count_steps(x, turns, desert, lambda x: x.endswith("Z"))
    for x in desert.keys()
    if x.endswith("A")
]
print(f"Part 2: {lcm(*part2_steps)}")
