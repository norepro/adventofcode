#!/usr/bin/python3

import networkx as nx

graph = nx.Graph()
with open("input.txt", "r") as f:
    for line in f:
        d = line.rstrip().split(":")
        for n in d[1].split():
            graph.add_edge(d[0], n)
_, partition = nx.stoer_wagner(graph)
print(f"Part 1: {len(partition[0]) * len(partition[1])}")
