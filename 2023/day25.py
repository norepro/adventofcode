#!/usr/bin/python3

import heapq
import networkx as nx
from collections import defaultdict
from tqdm import tqdm


class UndirectedGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(dict)

    def add_edge(self, a, b, weight=1):
        self.nodes.add(a)
        self.nodes.add(b)
        self.edges[a][b] = self.edges[b][a] = weight

    def delete_edge(self, a, b):
        if a in self.edges:
            del self.edges[a][b]
        if b in self.edges:
            del self.edges[b][a]

    def get_edge(self, a, b):
        edge = self.edges.get(a)
        return edge[b] if b in edge else None

    def get_edges(self, node):
        edges = self.edges[node]
        return list(zip(edges.keys(), edges.values()))

    def iterate_all_edges(self):
        for u in self.edges:
            for v in self.edges[u]:
                # Avoid duplicates by always favoring lower -> higher
                if u < v:
                    yield (u, v, self.edges[u][v])

    def delete_node(self, node):
        self.nodes.discard(node)
        for e in self.get_edges(node):
            self.delete_edge(e[0], node)

    def copy(self):
        graph = UndirectedGraph()
        graph.nodes = set(self.nodes)
        graph.edges = {}
        for e in self.edges:
            graph.edges[e] = self.edges[e].copy()
        return graph


# Implementation of Stoer-Wagner
# https://dl.acm.org/doi/pdf/10.1145/263867.263872
def maximum_adjacency_search(graph):
    start = next(iter(graph.nodes))
    visited = set([start])
    recent = [(start, 0), None]
    q = []
    qmap = {}
    for node, weight in graph.get_edges(start):
        heapq.heappush(q, (-weight, node))
        qmap[node] = -weight

    while len(visited) != len(graph.nodes):
        weight, node = heapq.heappop(q)
        if node in visited:
            continue
        visited.add(node)
        recent[1] = recent[0]
        recent[0] = (node, weight)
        for node, weight in graph.get_edges(node):
            if node not in visited:
                existing_weight = qmap.get(node) or 0
                heapq.heappush(q, (existing_weight - weight, node))
                qmap[node] = existing_weight - weight
    # (s, t, weight)
    return recent[1][0], recent[0][0], -recent[0][1]


def stoer_wagner(graph):
    # Copy the graph because we will be merging nodes
    original_graph = graph
    graph = graph.copy()

    best_cut_index = -1
    best_weight = float("inf")
    merges = []
    for i in tqdm(range(len(graph.nodes) - 1)):
        s, t, weight = maximum_adjacency_search(graph)
        merges.append((s, t))
        if weight < best_weight:
            best_cut_index = i
            best_weight = weight
        for e, weight in graph.get_edges(t):
            if e != s:
                existing_weight = graph.get_edge(s, e)
                if existing_weight is not None:
                    # s and t point to same node, add weights
                    graph.add_edge(s, e, weight + existing_weight)
                else:
                    # t points to node that s did not, add to s
                    graph.add_edge(s, e)
        graph.delete_node(t)
    # Find the nodes in one half of the best cut by replaying merges that led
    # up to it.
    best_partition = set([merges[best_cut_index][1]])
    for i in range(best_cut_index - 1, -1, -1):
        if merges[i][0] in best_partition:
            best_partition.add(merges[i][0])
            best_partition.add(merges[i][1])
    other_partition = original_graph.nodes.difference(best_partition)
    cut_edges = []
    for e in original_graph.iterate_all_edges():
        if (e[0] in best_partition and e[1] in other_partition) or (
            e[0] in other_partition and e[1] in best_partition
        ):
            cut_edges.append(e)
    # Emulate networkx return values for cleaner main code
    return cut_edges, (best_partition, other_partition)


USE_NETWORKX = False

graph = nx.Graph() if USE_NETWORKX else UndirectedGraph()
with open("input.txt", "r") as f:
    for line in f:
        d = line.rstrip().split(":")
        for n in d[1].split():
            graph.add_edge(d[0], n)
_, partition = nx.stoer_wagner(graph) if USE_NETWORKX else stoer_wagner(graph)
print(f"Part 1: {len(partition[0]) * len(partition[1])}")
