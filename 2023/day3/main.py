#!/usr/bin/python3

import re
from collections import defaultdict

SYMBOL_REGEX = r"[^\d\.]"
GEAR = "*"

id_total = 0
gear_ids = defaultdict(list)


def scan_for_symbols(str, id, x, y):
    symbol_matches = list(re.finditer(SYMBOL_REGEX, str))
    for symbol in symbol_matches:
        if symbol.group(0) == GEAR:
            gear_ids[(y, x + symbol.span()[0])].append(id)
    return len(symbol_matches) > 0


with open("input.txt", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    line = lines[i].strip()
    for m in re.finditer(r"\d+", line):
        is_id = False
        x1 = max(0, m.span()[0] - 1)
        x2 = min(len(line) - 1, m.span()[1] + 1)
        id = int(m.group(0))
        is_id = scan_for_symbols(line[x1], id, x1, i) | is_id
        is_id = scan_for_symbols(line[x2 - 1], id, x2 - 1, i) | is_id
        if i > 0:
            is_id = scan_for_symbols(lines[i - 1][x1:x2], id, x1, i - 1) | is_id
        if i < len(lines) - 1:
            is_id = scan_for_symbols(lines[i + 1][x1:x2], id, x1, i + 1) | is_id
        if is_id:
            id_total += id

gear_ratio_total = sum(
    [gear_ids[x][0] * gear_ids[x][1] for x in gear_ids if len(gear_ids[x]) == 2]
)

print(f"Part 1: {id_total}")
print(f"Part 2: {gear_ratio_total}")
