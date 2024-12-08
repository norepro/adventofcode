#!/usr/bin/python3

from collections import defaultdict


def get_antinodes(grid, a, b, include_harmonics=False):
    dx, dy = b[0] - a[0], b[1] - a[1]
    if include_harmonics:
        yield a
        yield b
    count = 0
    while count < 1 or include_harmonics:
        count += 1
        nx, ny = a[0] - dx * count, a[1] - dy * count
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            yield (nx, ny)
        else:
            break
    count = 0
    while count < 1 or include_harmonics:
        count += 1
        nx, ny = b[0] + dx * count, b[1] + dy * count
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            yield (nx, ny)
        else:
            break


grid = []
with open("input.txt") as f:
    for line in f:
        grid.append(list(line.strip()))
frequency_map = defaultdict(list)
for r, row in enumerate(grid):
    for c, col in enumerate(row):
        if col != '.':
            frequency_map[col].append((r, c))
nodes = set()
nodes_with_harmonics = set()
for freq in frequency_map:
    antennae = frequency_map[freq]
    antennae.sort()
    for i in range(0, len(antennae) - 1):
        for j in range(i + 1, len(antennae)):
            a, b = antennae[i], antennae[j]
            nodes.update(get_antinodes(grid, a, b))
            nodes_with_harmonics.update(get_antinodes(grid, a, b, True))

print(f"Part 1: {len(nodes)}")
print(f"Part 2: {len(nodes_with_harmonics)}")
