#!/usr/bin/python3

import functools


@functools.cache
def count_possible(icons, counts):
    if len(icons) == 0:
        return 1 if len(counts) == 0 else 0
    if icons[0] == "#":
        if len(counts) == 0:
            # Unexpected spring
            return 0
        if counts[0] > len(icons):
            # Not enough space for required springs
            return 0
        for i in range(1, counts[0]):
            if icons[i] == ".":
                # Not enough springs for current count
                return 0
        if counts[0] < len(icons):
            if icons[counts[0]] == "#":
                # Spring count is larger than expected
                return 0
            if len(counts) > 1 and len(icons) <= counts[0] + 1:
                # Must have room for more groups
                return 0
        # More icons to check
        return count_possible("." + icons[counts[0] + 1 :], counts[1:])
    elif icons[0] == ".":
        # Nothing interesting, go to next icon
        return count_possible(icons[1:], counts)
    else:
        # Check both spring and not spring
        sc = count_possible("#" + icons[1:], counts)
        nc = count_possible("." + icons[1:], counts)
        return sc + nc


records = []
with open("input.txt", "r") as f:
    for line in f:
        icons, counts = line.rstrip().split()
        records.append((icons, tuple(map(int, counts.split(",")))))
total = sum([count_possible(r[0], r[1]) for r in records])
print(f"Part 1: {total}")

total = sum([count_possible(((r[0] + "?") * 5)[:-1], r[1] * 5) for r in records])
print(f"Part 2: {total}")
