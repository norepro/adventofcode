#!/usr/bin/python3


def find_trails(grid, row, col, dests, unique, prev=-1):
    if row < 0 or col < 0 or row >= len(grid) or col >= len(
            grid[row]) or grid[row][col] != prev + 1:
        return
    v = grid[row][col]
    if v == 9:
        unique[0] += 1
        dests.add((row, col))
        return
    find_trails(grid, row - 1, col, dests, unique, v)
    find_trails(grid, row + 1, col, dests, unique, v)
    find_trails(grid, row, col - 1, dests, unique, v)
    find_trails(grid, row, col + 1, dests, unique, v)


with open("input.txt") as f:
    grid = [list(map(int, line.rstrip())) for line in f]

p1, p2 = 0, 0
for x, row in enumerate(grid):
    for y, col in enumerate(row):
        if col == 0:
            dests = set()
            unique = [0]
            find_trails(grid, x, y, dests, unique)
            p1 += len(dests)
            p2 += unique[0]

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
