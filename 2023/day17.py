#!/usr/bin/python3

import networkx as nx

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
ALL_DIRS = [NORTH, EAST, SOUTH, WEST]


def print_grid(grid, nodes):
    grid = grid.copy()
    for i in range(1, len(nodes)):
        nx = nodes[i - 1]
        ny = nodes[i]
        if nx[0] == ny[0]:
            d = 1 if ny[1] > nx[1] else -1
            for x in range(nx[1] + d, ny[1] + d, d):
                grid[nx[0]][x] = "."
        else:
            d = 1 if ny[0] > nx[0] else -1
            for x in range(nx[0] + d, ny[0] + d, d):
                grid[x][nx[1]] = "."
    for row in grid:
        for col in row:
            print(col, end="")
        print()
    print()


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_opposite_dir(dir):
    return ALL_DIRS[(dir + 2) % len(ALL_DIRS)]


def get_cost(grid, row1, col1, row2, col2):
    if row1 == row2:
        d = 1 if col2 > col1 else -1
        return sum([grid[row1][c] for c in range(col1 + d, col2 + d, d)])
    elif col1 == col2:
        d = 1 if row2 > row1 else -1
        return sum([grid[r][col1] for r in range(row1 + d, row2 + d, d)])
    raise RuntimeError("Diagonal cost")


def get_row_col(row, col, dir, count):
    if dir == NORTH:
        row -= count
    elif dir == EAST:
        col += count
    elif dir == SOUTH:
        row += count
    else:
        col -= count
    return row, col


def is_valid(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def grid_to_graph(grid, min_dir_count, max_dir_count):
    graph = nx.DiGraph()
    # Add all nodes and the directions they are approached
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            for dir in ALL_DIRS:
                graph.add_node((row, col, dir))
    # Add edges to each possible "must turn" node
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            for in_dir in ALL_DIRS:
                edges = []
                for out_dir in ALL_DIRS:
                    if in_dir == out_dir:
                        # No U-turns
                        continue
                    opp_dir = get_opposite_dir(out_dir)
                    if (row != 0 or col != 0) and in_dir == opp_dir:
                        # Must turn, cannot continue in this direction
                        continue
                    for c in range(min_dir_count, max_dir_count + 1):
                        new_row, new_col = get_row_col(row, col, out_dir, c)
                        if not is_valid(grid, new_row, new_col):
                            break
                        cost = get_cost(grid, row, col, new_row, new_col)
                        edges.append(
                            ((row, col, in_dir), (new_row, new_col, opp_dir), cost)
                        )
                graph.add_weighted_edges_from(edges)
    return graph


grid = []
with open("input.txt", "r") as f:
    for line in f:
        grid.append(list(map(int, list(line.rstrip()))))

src = (0, 0, WEST)
dst_row = len(grid) - 1
dst_col = len(grid[0]) - 1

graph = grid_to_graph(grid, 1, 3)
min_loss = min(
    nx.astar_path_length(graph, src, (dst_row, dst_col, NORTH), heuristic),
    nx.astar_path_length(graph, src, (dst_row, dst_col, WEST), heuristic),
)
print(f"Part 1: {min_loss}")

graph = grid_to_graph(grid, 4, 10)
min_loss = min(
    nx.astar_path_length(graph, src, (dst_row, dst_col, NORTH), heuristic),
    nx.astar_path_length(graph, src, (dst_row, dst_col, WEST), heuristic),
)
print(f"Part 2: {min_loss}")
