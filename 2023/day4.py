#!/usr/bin/python3

import re
from collections import defaultdict

point_total = 0
copies = defaultdict(int)
with open("input.txt", "r") as f:
    for line in f:
        m = re.search(r"Card\s+(\d+):\s+([\d\s]+)\s+\|\s+([\d\s]+)", line)
        id = int(m.group(1))
        copies[id] += 1
        winning_nums = set(m.group(2).split())
        actual_nums = set(m.group(3).split())
        n = len(winning_nums.intersection(actual_nums))
        if n == 0:
            continue
        for ncopy in range(copies[id]):
            if ncopy == 0:
                point_total += 2 ** (n - 1)
            for i in range(n):
                copies[id + i + 1] += 1
print(f"Part 1: {point_total}")
print(f"Part 2: {sum(copies.values())}")
