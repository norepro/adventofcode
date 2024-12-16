#!/usr/bin/python3

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

SIDE_NODES = {
    NORTH: (False, True),
    SOUTH: (False, True),
    EAST: (True, False),
    WEST: (True, False),
}


class Plot:

    def __init__(self, id):
        self.id = id
        self.area = 0
        self.perimeter = 0
        self.sides = 0

    def __repr__(self) -> str:
        return f"Plot({self.id},{self.area},{self.perimeter},{self.sides})"


def get_neighbors(grid,
                  row,
                  col,
                  ns=True,
                  ew=True,
                  until_wall=False,
                  req_edge=None):
    c = grid[row][col]
    max_n = 999 if until_wall else 1
    check = lambda rx, ry: has_edge(
        grid, rx, ry, req_edge) if req_edge != None else lambda _, __: True
    if ns:
        n, x = 0, row - 1
        while n < max_n and x >= 0 and grid[x][col] == c and check(x, col):
            yield (x, col)
            x -= 1
            n += 1
        n, x = 0, row + 1
        while n < max_n and x < len(grid) and grid[x][col] == c and check(
                x, col):
            yield (x, col)
            x += 1
            n += 1
    if ew:
        n, x = 0, col - 1
        while n < max_n and x >= 0 and grid[row][x] == c and check(row, x):
            yield (row, x)
            x -= 1
            n += 1
        n, x = 0, col + 1
        while n < max_n and x < len(grid[row]) and grid[row][x] == c and check(
                row, x):
            yield (row, x)
            x += 1
            n += 1


def get_edges(grid, row, col):
    c = grid[row][col]
    if row == 0 or grid[row - 1][col] != c:
        yield NORTH
    if row >= len(grid) - 1 or grid[row + 1][col] != c:
        yield SOUTH
    if col == 0 or grid[row][col - 1] != c:
        yield WEST
    if col >= len(grid[row]) - 1 or grid[row][col + 1] != c:
        yield EAST


def has_edge(grid, row, col, edge):
    for e in get_edges(grid, row, col):
        if edge == e:
            return True
    return False


def get_area_perimeter(grid, row, col, plant, plot, plot_ids):
    if plot_ids[row][col] != -1:
        return
    plot_ids[row][col] = plot.id
    plot.area += 1
    for e in get_edges(grid, row, col):
        plot.perimeter += 1
        sn = SIDE_NODES[e]
        already_counted_side = False
        for n in get_neighbors(grid, row, col, sn[0], sn[1], True, e):
            if plot_ids[n[0]][n[1]] == plot.id:
                already_counted_side = True
        if not already_counted_side:
            plot.sides += 1

    for n in get_neighbors(grid, row, col):
        get_area_perimeter(grid, n[0], n[1], plant, plot, plot_ids)


with open("input.txt") as f:
    grid = [list(line.rstrip()) for line in f]

cur_plot_id = 0
plot_ids = [[-1] * len(x) for x in grid]
plots = {}
for x, row in enumerate(grid):
    for y, col in enumerate(row):
        if plot_ids[x][y] == -1:
            plot = Plot(cur_plot_id)
            plots[plot.id] = plot
            cur_plot_id += 1
            get_area_perimeter(grid, x, y, col, plot, plot_ids)

s = sum([plots[x].area * plots[x].perimeter for x in plots])
print(f"Part 1: {s}")
s = sum([plots[x].area * plots[x].sides for x in plots])
print(f"Part 2: {s}")
