#!/usr/bin/python3

import re
from tqdm import tqdm


def gen_results(values, target, current, i, use_concat=False):
    if i == len(values) - 1 or current > target:
        yield current
    elif i < len(values) - 1:
        if use_concat:
            yield from gen_results(values, target,
                                   int(f"{current}{values[i + 1]}"), i + 1,
                                   use_concat)
        yield from gen_results(values, target, current + values[i + 1], i + 1,
                               use_concat)
        yield from gen_results(values, target, current * values[i + 1], i + 1,
                               use_concat)


p1, p2 = 0, 0
values = []
with open("input.txt") as f:
    for line in f:
        values.append(list(map(int, re.split(r':?\s+', line.strip()))))

for value in tqdm(values):
    for result in gen_results(value[1:], value[0], value[1], 0):
        if result == value[0]:
            p1 += result
            break
    else:
        for result in gen_results(value[1:], value[0], value[1], 0, True):
            if result == value[0]:
                p2 += result
                break

print(f"Part 1: {p1}")
print(f"Part 2: {p1 + p2}")
