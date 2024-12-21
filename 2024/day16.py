#!/usr/bin/python3

from collections import defaultdict
from queue import PriorityQueue

SOUTH, NORTH, EAST, WEST = 0, 1, 2, 3
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Node:

    def __init__(self, pos, cost, dir, path):
        self.pos = pos
        self.cost = cost
        self.dir = dir
        self.path = path

    def __lt__(self, other):
        return self.cost < other.cost

    def __repr__(self) -> str:
        return f"Node({self.pos},{self.cost},{self.dir},{self.path})"


def find_cheapest_length_and_nodes(grid, start, end):
    cheapest = float('inf')
    cheapest_per_pos = defaultdict(lambda: float('inf'))
    cheapest_nodes = set()
    q = PriorityQueue()
    q.put(Node(start, 0, EAST, set([start])))
    while not q.empty():
        node = q.get()
        if node.cost > cheapest:
            # Path is too expensive already
            continue
        if cheapest_per_pos[(node.pos, node.dir)] < node.cost:
            # Cheaper path to current node from this direction
            # already exists
            continue
        cheapest_per_pos[(node.pos, node.dir)] = node.cost
        for nb in get_neighbors(grid, node.pos):
            dir = get_dir(node.pos, nb)
            cost_delta = 1 if dir == node.dir else 1001
            cost = node.cost + cost_delta

            if nb == end:
                if cost < cheapest:
                    cheapest = cost
                    cheapest_nodes.clear()
                    cheapest_nodes.update(node.path)
                    cheapest_nodes.add(end)
                elif cost == cheapest:
                    cheapest_nodes.update(node.path)
            elif nb not in node.path:
                if cost < cheapest:
                    path = set(node.path)
                    path.add(nb)
                    q.put(Node(nb, cost, dir, path))
    return cheapest, cheapest_nodes


def get_dir(a, b):
    if a[0] == b[0]:
        return EAST if b[1] > a[1] else WEST
    return SOUTH if b[0] > a[0] else NORTH


def get_neighbors(grid, pos):
    if pos[0] > 0 and grid[pos[0] - 1][pos[1]] != '#':
        yield (pos[0] - 1, pos[1])
    if pos[0] < len(grid) - 1 and grid[pos[0] + 1][pos[1]] != '#':
        yield (pos[0] + 1, pos[1])
    if pos[1] > 0 and grid[pos[0]][pos[1] - 1] != '#':
        yield (pos[0], pos[1] - 1)
    if pos[1] < len(grid[pos[0]]) - 1 and grid[pos[0]][pos[1] + 1] != '#':
        yield (pos[0], pos[1] + 1)


with open("input.txt") as f:
    grid = [list(s) for s in f.read().rstrip().split('\n')]
for r, row in enumerate(grid):
    for c, col in enumerate(row):
        if col == 'S':
            start = (r, c)
        elif col == 'E':
            end = (r, c)
cheapest, cheapest_nodes = find_cheapest_length_and_nodes(grid, start, end)
print(f"Part 1: {cheapest}")
print(f"Part 2: {len(cheapest_nodes)}")
