#!/usr/bin/python3

import re
from collections import defaultdict

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14
possible_id_total = 0
power_total = 0

with open("input.txt", "r") as f:
    for line in f:
        m = re.search(r"Game (\d+): (.+)", line)
        id = int(m.group(1))
        counts = defaultdict(int)
        for n, color in re.findall(r"(\d+)\s+(red|green|blue)", m.group(2)):
            counts[color] = max(int(n), counts[color])
        if (
            counts["red"] <= MAX_RED
            and counts["green"] <= MAX_GREEN
            and counts["blue"] <= MAX_BLUE
        ):
            possible_id_total += id
        power_total += counts["red"] * counts["green"] * counts["blue"]
print(f"Part 1: {possible_id_total}")
print(f"Part 2: {power_total}")
