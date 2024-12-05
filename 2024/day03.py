#!/usr/bin/python3

import re

p1, p2 = 0, 0
with open("input.txt") as f:
    enabled = True
    for line in f:
        for m in re.finditer(r'do\(\)|don\'t\(\)|mul\((\d+),(\d+)\)', line):
            if m.group(0) == 'do()':
                enabled = True
            elif m.group(0) == 'don\'t()':
                enabled = False
            else:
                product = int(m.group(1)) * int(m.group(2))
                p1 += product
                if enabled:
                    p2 += product
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
