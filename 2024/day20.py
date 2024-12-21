#!/usr/bin/python3

from collections import namedtuple
from tqdm import tqdm

CheatTime = namedtuple('CheatTime', ['start', 'end', 'time'])

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def make_race(grid):
    race = []
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 'S':
                race.append((r, c))
                break
        if len(race) == 1:
            break
    while True:
        for dir in DIRS:
            n = (race[-1][0] + dir[0], race[-1][1] + dir[1])
            if grid[n[0]][n[1]] != '#':
                if len(race) > 1 and n == race[-2]:
                    continue
                race.append(n)
                break
        if grid[race[-1][0]][race[-1][1]] == 'E':
            break
    return race


def get_cheat_times(race, dist, min_savings):
    race_index = {pos: i for i, pos in enumerate(race)}
    for n in tqdm(race):
        for candidate in get_nodes_within_x(n, race, race_index, dist,
                                            min_savings):
            savings = get_shortest_path_length(race_index, n, candidate)
            if savings >= dist:
                yield CheatTime(n, candidate, savings)


def get_shortest_path_length(race_index, a, b):
    return abs(race_index[a] - race_index[b]) - manhattan(a, b)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_nodes_within_x(pos, path, path_index, x, min_savings):
    pos_idx = path_index[pos]
    pi = pos_idx + min_savings
    while pi < len(path):
        p = path[pi]
        d = manhattan(pos, p)
        if 1 < d <= x and pos_idx + d + min_savings <= pi:
            yield p
        pi += max(1, d - x)


with open("input.txt") as f:
    grid = [list(x.rstrip()) for x in f.readlines()]
race = make_race(grid)

total = 0
for _ in get_cheat_times(race, 2, 100):
    total += 1
print(f"Part 1: {total}")

total = 0
for _ in get_cheat_times(race, 20, 100):
    total += 1
print(f"Part 2: {total}")
