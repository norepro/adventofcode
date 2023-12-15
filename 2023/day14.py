#!/usr/bin/python3

import numpy as np


def tilt_north(grid):
    for row in range(1, len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != "O":
                continue
            for r in range(row - 1, -1, -1):
                if grid[r][col] != ".":
                    break
            if r == 0 and grid[r][col] == ".":
                r = -1
            grid[row][col] = "."
            grid[r + 1][col] = "O"


def to_grid_string(grid):
    return "|".join(map("".join, grid))


def from_grid_string(grid_string):
    return list(map(list, grid_string.split("|")))


def spin_cycle(grid_string):
    grid = from_grid_string(grid_string)
    for i in range(4):
        tilt_north(grid)
        grid = np.rot90(grid, k=1, axes=(1, 0))
    return to_grid_string(grid)


def get_load(grid):
    load = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "O":
                load += len(grid) - row
    return load


grid = []
with open("input.txt", "r") as f:
    for line in f:
        grid.append(list(line.rstrip()))
tilt_north(grid)
print(f"Part 1: {get_load(grid)}")

seen = {}
grid_string = to_grid_string(grid)
num_cycles = 1_000_000_000
for i in range(num_cycles):
    if grid_string in seen:
        period = i - seen[grid_string]
        target_cycle = period + num_cycles % period
        grid_string = [x for x in seen if seen[x] == target_cycle][0]
        break
    else:
        seen[grid_string] = i
        grid_string = spin_cycle(grid_string)
print(f"Part 2: {get_load(from_grid_string(grid_string))}")
