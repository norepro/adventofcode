#!/usr/bin/env python3

import networkx as nx
from itertools import combinations


def make_graph(computers):
    g = nx.Graph()
    for c in computers:
        g.add_edge(c[0], c[1])
    return g


def get_triangles(g):
    triangles = set()
    for n in nx.triangles(g):
        for n1, n2 in combinations(list(g.neighbors(n)), 2):
            if g.has_edge(n1, n2):
                triangles.add(tuple(sorted((n, n1, n2))))
    return triangles


with open("input.txt") as f:
    computers = [x.rstrip().split('-') for x in f]
g = make_graph(computers)
triangles = get_triangles(g)
p1 = 0
for t in triangles:
    if any(x.startswith('t') for x in t):
        p1 += 1
print(f"Part 1: {p1}")

largest_clique = (0, )
for clique in nx.find_cliques(g):
    if len(clique) > len(largest_clique):
        largest_clique = clique
print(f"Part 2: {','.join(sorted(largest_clique))}")
