#!/usr/bin/python3

from functools import reduce


def get_priority(c):
    o = ord(c)
    return o - 96 if o >= 96 else o - 38


def get_common_item(*sacks):
    common = reduce(lambda a, b: set(a).intersection(set(b)), sacks)
    return next(iter(common))


split_total = 0
group_total = 0

with open("input.txt", "r") as f:
    group_index = 0
    group_sacks = []
    for line in f:
        line = line.strip()
        n = int(len(line) / 2)
        split_total += get_priority(get_common_item(line[:n], line[n:]))
        group_sacks.append(line)
        group_index += 1
        if group_index == 3:
            group_total += get_priority(
                get_common_item(group_sacks[0], group_sacks[1], group_sacks[2])
            )
            group_index = 0
            group_sacks.clear()
print(f"Part 1: {split_total}")
print(f"Part 2: {group_total}")
