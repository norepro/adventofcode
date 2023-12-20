#!/usr/bin/python3

import re
from collections import defaultdict

id_total = 0
gear_ids = defaultdict(list)


def scan_for_symbols(chars, id, row, col):
    is_id = False
    for i in range(len(chars)):
        for j in range(len(chars[i])):
            c = chars[i][j]
            if not c.isdigit() and c != ".":
                is_id = True
            if c == "*":
                gear_ids[(row + i, col + j)].append(id)
    return is_id


with open("input.txt", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    line = lines[i].strip()
    for m in re.finditer(r"\d+", line):
        id = int(m.group(0))
        row = max(0, i - 1)
        row_max = min(len(lines), i + 2)
        col = max(0, m.span()[0] - 1)
        col_max = min(len(line), m.span()[1] + 1)
        chars = [lines[i][col:col_max] for i in range(row, row_max)]
        if scan_for_symbols(chars, id, row, col):
            id_total += id

gear_ratio_total = sum(
    [gear_ids[x][0] * gear_ids[x][1] for x in gear_ids if len(gear_ids[x]) == 2]
)

print(f"Part 1: {id_total}")
print(f"Part 2: {gear_ratio_total}")
