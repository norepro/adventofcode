#!/usr/bin/python3

import re

s1, s2 = [], []
with open("input.txt") as f:
    for line in f:
        m = re.search(r"^(\d+)\s+(\d+)", line)
        s1.append(int(m.group(1)))
        s2.append(int(m.group(2)))
s1 = sorted(s1)
s2 = sorted(s2)
p1, p2, j = 0, 0, 0
for i in range(len(s1)):
    p1 += abs(s1[i] - s2[i])
    while j < len(s2) and s2[j] < s1[i]:
        j += 1
    k = j
    while k < len(s2) and s2[k] == s1[i]:
        k += 1
    p2 += s1[i] * (k - j)
    j = k
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
