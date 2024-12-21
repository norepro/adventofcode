#!/usr/bin/python3

import networkx as nx


def make_graph(coords, size):
    g = nx.Graph()
    walls = set(coords)
    for x in range(size):
        for y in range(size):
            o = (x, y)
            if o in walls:
                continue
            c = (x + 1, y)
            if c not in walls:
                g.add_edge(o, c)
            c = (x, y + 1)
            if c not in walls:
                g.add_edge(o, c)
    return g


SIZE = 70
NUM_FALLS = 1024
START = (0, 0)
END = (SIZE, SIZE)

with open("input.txt") as f:
    coords = [tuple(map(int, x.split(','))) for x in f]
g = make_graph(coords[:NUM_FALLS], SIZE + 1)
path = nx.shortest_path(g, START, END)
print(f"Part 1: {len(path) - 1}")

for i in range(NUM_FALLS, len(coords)):
    if g.has_node(coords[i]):
        g.remove_node(coords[i])
        if coords[i] in path:
            try:
                path = nx.shortest_path(g, START, END)
            except nx.exception.NetworkXNoPath:
                print(f"Part 2: {coords[i]}")
                break
