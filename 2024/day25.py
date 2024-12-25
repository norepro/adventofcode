#!/usr/bin/env python3


def make_lock_key(grid):
    sums = [0] * 5
    for i, line in enumerate(grid.split('\n')):
        if i == 0:
            is_lock = line == '#####'
        elif i < 6:
            for ci, c in enumerate(line):
                if c == '#':
                    sums[ci] += 1
    return is_lock, sums


with open("input.txt") as f:
    grids = f.read().split('\n\n')
locks, keys = [], []
for grid in grids:
    x = make_lock_key(grid)
    if x[0]:
        locks.append(x[1])
    else:
        keys.append(x[1])
n = 0
for lock in locks:
    for key in keys:
        for i in range(5):
            if lock[i] + key[i] > 5:
                break
        else:
            n += 1
print(f"Part 1: {n}")
