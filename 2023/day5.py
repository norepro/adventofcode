#!/usr/bin/python3

import re


def transform_single_phase(seed_ranges, phase_ranges):
    new_ranges = []
    pending = seed_ranges.copy()
    while len(pending) > 0:
        found_intersection = False
        seed_range = pending.pop()
        for phase_range in phase_ranges:
            pr_src, pr_dst, n = phase_range

            # Find intersection of seed range and phase input range
            #      |--pr_src + n--|
            # |--seed_range--|
            #      |         |
            #    i_start    i_end
            i_start = max(seed_range[0], pr_src)
            i_end = min(seed_range[0] + seed_range[1], pr_src + n)
            if i_start >= i_end:
                continue
            found_intersection = True

            # transform [i_start, i_end]
            new_ranges.append(
                (
                    i_start + pr_dst - pr_src,
                    i_end - i_start,
                )
            )

            # enqueue parts of seed_range left or right of the intersection
            if i_start > seed_range[0]:
                pending.append((seed_range[0], i_start - seed_range[0]))

            if i_end < seed_range[0] + seed_range[1]:
                pending.append((i_end, seed_range[0] + seed_range[1] - i_end))
            break

        if not found_intersection:
            # no transform, return identity transform
            new_ranges.append((seed_range[0], seed_range[1]))
    return new_ranges


def transform_all_phases(seed_ranges, phases):
    for phase_ranges in phases:
        seed_ranges = transform_single_phase(seed_ranges, phase_ranges)
    return seed_ranges


phases = []

with open("input.txt", "r") as f:
    for line in f:
        if line.startswith("seeds:"):
            seeds = [int(x) for x in re.findall(r"\d+", line)]
            continue
        if ":" in line:
            phase_ranges = []
            phases.append(phase_ranges)
            continue
        m = re.findall(r"\d+", line)
        if len(m) > 0:
            dst_start, src_start, n = [int(x) for x in m]
            phase_ranges.append((src_start, dst_start, n))

part1_ranges = [(x, 1) for x in seeds]
part2_ranges = [(x, y) for x, y in zip(seeds[::2], seeds[1::2])]
print(f"Part 1: {min(transform_all_phases(part1_ranges, phases))[0]}")
print(f"Part 2: {min(transform_all_phases(part2_ranges, phases))[0]}")
