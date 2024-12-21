#!/usr/bin/python3

from tqdm import tqdm
from functools import cache


@cache
def is_possible(towels, pattern):
    if len(pattern) == 0:
        return 1
    ways = 0
    for t in towels:
        if pattern.startswith(t):
            ways += is_possible(towels, pattern[len(t):])
    return ways


with open("input.txt") as f:
    data = f.read().splitlines()
towels = tuple(data[0].split(', '))

p1, p2 = 0, 0
for pattern in tqdm(data[2:]):
    ways = is_possible(towels, pattern)
    if ways > 0:
        p1 += 1
        p2 += ways
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
