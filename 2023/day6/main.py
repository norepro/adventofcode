#!/usr/bin/python3

import re
import math
from functools import reduce


def count_wins(time, record):
    d = math.sqrt((time**2) - (4 * record))
    t1 = (time + d) / 2
    t2 = (time - d) / 2
    return math.floor(t1) - math.ceil(t2) + 1


with open("input.txt", "r") as f:
    data_part1 = []
    data_part2 = []
    for line in f:
        data_part1.append([int(x) for x in re.findall("\d+", line)])
        data_part2.append(int(re.search(r"[\d\s]+", line).group().replace(" ", "")))
    data_part1 = list(zip(data_part1[0], data_part1[1]))

part1_product = reduce(lambda a, b: a * count_wins(b[0], b[1]), data_part1, 1)
print(f"Part 1: {part1_product}")
print(f"Part 2: {count_wins(data_part2[0], data_part2[1])}")
