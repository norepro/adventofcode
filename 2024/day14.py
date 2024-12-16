#!/usr/bin/python3

import re
from collections import defaultdict
from math import prod

ROWS, COLS = 103, 101


class Grid:

    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self._crow = nrows // 2
        self._ccol = ncols // 2
        self._plot = [[0] * ncols for _ in range(nrows)]

    def get_quadrant(self, position):
        row = position[1] % self.nrows
        col = position[0] % self.ncols
        if row == self._crow or col == self._ccol:
            return -1
        if row < self._crow:
            return 0 if col < self._ccol else 1
        return 3 if col < self._ccol else 2

    def set_robot(self, position):
        col = position[0] % self.ncols
        row = position[1] % self.nrows
        self._plot[row][col] += 1

    def reset_plot(self):
        for row in self._plot:
            for i in range(len(row)):
                row[i] = 0

    def plot_points(self):
        for y, row in enumerate(self._plot):
            for x, col in enumerate(row):
                if col != 0:
                    yield (x, y, col)

    def get_variances(self):
        n_points, sum_x, sum_y = 0, 0, 0
        for x, y, _ in self.plot_points():
            n_points += 1
            sum_x += x
            sum_y += y
        avg_x, avg_y = sum_x / n_points, sum_y / n_points
        sum_sq_x, sum_sq_y = 0, 0
        for x, y, _ in self.plot_points():
            sum_sq_x += (x - avg_x)**2
            sum_sq_y += (y - avg_y)**2
        return (sum_sq_x / n_points, sum_sq_y / n_points)

    def print_plot(self, find_tree=False):
        for y in range(self.nrows):
            for x in range(self.ncols):
                if not find_tree and (x == self._ccol or y == self._crow):
                    print(" ", end='')
                    continue
                r = self._plot[y][x]
                if r == 0:
                    print(".", end='')
                else:
                    print("#" if find_tree else r, end='')
            print()


class Robot:

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __repr__(self) -> str:
        return f"Robot({self.position},{self.velocity})"

    def position_after(self, seconds, persist=False):
        x = self.position[0] + seconds * self.velocity[0]
        y = self.position[1] + seconds * self.velocity[1]
        p = (x, y)
        if persist:
            self.position = p
        return p


robots = []
grid = Grid(ROWS, COLS)
with open("input.txt") as f:
    for line in f:
        px, py, dx, dy = list(map(int, re.findall(r'(-?\d+)', line)))
        robots.append(Robot((px, py), (dx, dy)))

quad_counts = defaultdict(int)
for robot in robots:
    p = robot.position_after(100)
    quad_counts[grid.get_quadrant(p)] += 1

min_x_var, min_y_var = 99999, 99999
min_x_secs, min_y_secs = 0, 0

# Find minimum variance of x and y and their respective times
for nsecs in range(max(grid.nrows, grid.ncols)):
    grid.reset_plot()
    for robot in robots:
        p = robot.position_after(1, True)
        grid.set_robot(p)
    var = grid.get_variances()
    if var[0] < min_x_var:
        min_x_secs = nsecs
        min_x_var = var[0]
    if var[1] < min_y_var:
        min_y_secs = nsecs
        min_y_var = var[1]

# Find time when minimum x and y variances converge
for nsecs in range(min_x_secs + 1, 100000, grid.ncols):
    if nsecs % grid.nrows == min_y_secs + 1:
        break
product = prod([quad_counts[q] for q in quad_counts if q != -1])
print(f"Part 1: {product}")
print(f"Part 2: {nsecs}")
