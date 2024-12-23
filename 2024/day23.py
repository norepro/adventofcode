#!/usr/bin/env python3

import networkx as nx

with open("input.txt") as f:
    g = nx.Graph(x.rstrip().split('-') for x in f)
sum_three = 0
largest = (0, )
for clique in nx.enumerate_all_cliques(g):
    if len(clique) == 3 and any(x.startswith('t') for x in clique):
        sum_three += 1
    if len(clique) > len(largest):
        largest = clique
print(f"Part 1: {sum_three}")
print(f"Part 2: {','.join(sorted(largest))}")
