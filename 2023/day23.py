#!/usr/bin/python3

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3


class Node:
    def __init__(self, location, tile):
        self.location = location
        self.tile = tile
        self.edges = {}

    def __repr__(self) -> str:
        return f"Node({self.location},{self.tile})"


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.location] = node


def dfs_longest_length(graph, current, end, current_length=0, visited=None):
    if current == end:
        return current_length
    visited = visited or set()
    if current in visited:
        return 0
    visited.add(current)
    max_length = 0
    for neighbor in graph.nodes[current].edges:
        nloc = neighbor.location
        length = graph.nodes[current].edges[neighbor]
        max_length = max(
            max_length,
            dfs_longest_length(graph, nloc, end, current_length + length, visited),
        )
    visited.remove(current)
    return max_length


def create_graph(tiles, use_slopes=False):
    graph = Graph()
    for loc, tile in tiles:
        node = Node(loc, tile)
        graph.add_node(node)

    for loc in graph.nodes:
        node = graph.nodes[loc]
        if use_slopes:
            match node.tile:
                case ".":
                    neighbors = [
                        ((loc[0] + 1, loc[1]), SOUTH),
                        ((loc[0] - 1, loc[1]), NORTH),
                        ((loc[0], loc[1] + 1), EAST),
                        ((loc[0], loc[1] - 1), WEST),
                    ]
                case ">":
                    neighbors = [((loc[0], loc[1] + 1), EAST)]
                case "<":
                    neighbors = [((loc[0], loc[1] - 1), WEST)]
                case "v":
                    neighbors = [((loc[0] + 1, loc[1]), SOUTH)]
                case _:
                    continue
        else:
            neighbors = [
                ((loc[0] + 1, loc[1]), SOUTH),
                ((loc[0] - 1, loc[1]), NORTH),
                ((loc[0], loc[1] + 1), EAST),
                ((loc[0], loc[1] - 1), WEST),
            ]
        for n, dir in neighbors:
            if n not in graph.nodes:
                continue
            n = graph.nodes[n]
            if use_slopes:
                if (
                    n.tile == "."
                    or (n.tile == ">" and dir != WEST)
                    or (n.tile == "<" and dir != EAST)
                    or (n.tile == "v" and dir != NORTH)
                ):
                    node.edges[n] = 1  # Length
            else:
                node.edges[n] = 1
    return graph


def reduce_graph(graph):
    made_adjustments = True
    # Reduce the graph to only intersections
    while made_adjustments:
        made_adjustments = False
        to_remove = []
        for loc in graph.nodes:
            node = graph.nodes[loc]
            if len(node.edges) == 2:
                a, b = node.edges.keys()
                length = sum(node.edges.values())
                a.edges[b] = length
                b.edges[a] = length
                if node in a.edges:
                    del a.edges[node]
                if node in b.edges:
                    del b.edges[node]
                to_remove.append(node.location)
                made_adjustments = True
        for loc in to_remove:
            del graph.nodes[loc]
    # Prune any edges that no longer point to valid nodes
    for loc in graph.nodes:
        node = graph.nodes[loc]
        for n in list(node.edges.keys()):
            if n.location not in graph.nodes:
                del node.edges[n]


tiles = []
with open("input.txt", "r") as f:
    row = 0
    for line in f:
        for col, c in enumerate(line.rstrip()):
            if c != "#":
                tiles.append(((row, col), c))
        row += 1

start = min(tiles)[0]
end = max(tiles)[0]

graph = create_graph(tiles, True)
reduce_graph(graph)
steps = dfs_longest_length(graph, start, end)
print(f"Part 1: {steps}")

graph = create_graph(tiles)
reduce_graph(graph)
steps = dfs_longest_length(graph, start, end)
print(f"Part 2: {steps}")
