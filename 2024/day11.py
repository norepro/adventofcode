#!/usr/bin/python3

import math
from functools import cache


def get_blink(stone):
    if stone == 0:
        return (1, )
    else:
        n = int(math.log10(stone)) + 1
        if n % 2 == 0:
            n = int(n / 2)
            return (int(stone / (10**n)), stone % (10**n))
        else:
            return (stone * 2024, )


@cache
def blink(stone, i, max_i):
    if i >= max_i:
        return 1
    new_stones = get_blink(stone)
    n = blink(new_stones[0], i + 1, max_i)
    if len(new_stones) == 2:
        return n + blink(new_stones[1], i + 1, max_i)
    else:
        return n


with open("input.txt") as f:
    stones = list(map(int, f.read().split()))

p1, p2 = 0, 0
for stone in stones:
    p1 += blink(stone, 0, 25)
    p2 += blink(stone, 0, 75)

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
