#!/usr/bin/python3

from tqdm import tqdm

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
OBSTACLE, VOID, GUARD = '#', '0', '^'
EXITED, LOOP, CONTINUE = 0, 1, 2


class Grid:

    def __init__(self, grid):
        self.grid = grid
        self.seen = []
        for row in range(len(grid)):
            self.seen.append([])
            for col in range(len(grid[row])):
                self.seen[row].append([])
                if grid[row][col] == GUARD:
                    self.guard_row, self.guard_col = row, col
                    self.original_row, self.original_col = row, col
                    self.guard_dir = UP
                    self.seen[row][col].append(UP)
        self.__obs_row = 0
        self.__obs_col = 0
        self.__obs_orig = self.grid[0][0]

    def move(self):
        next_step, row, col = self.__get_next_step()
        while next_step == OBSTACLE:
            self.__turn()
            next_step, row, col = self.__get_next_step()
        while next_step != VOID and next_step != OBSTACLE:
            self.guard_row, self.guard_col = row, col
            seen = self.seen[row][col]
            if self.guard_dir in seen:
                return LOOP
            seen.append(self.guard_dir)
            next_step, row, col = self.__get_next_step()
        if next_step == VOID:
            return EXITED
        return CONTINUE

    def get_seen_coords(self):
        coords = []
        for row, row_data in enumerate(self.seen):
            for col, col_data in enumerate(row_data):
                if len(col_data) > 0:
                    coords.append((row, col))
        return coords

    def reset(self):
        for row in self.seen:
            for col in row:
                col.clear()
        self.guard_col = self.original_col
        self.guard_row = self.original_row
        self.guard_dir = UP
        self.grid[self.__obs_row][self.__obs_col] = self.__obs_orig

    def set_obstacle(self, row, col):
        cur = self.grid[row][col]
        if cur == OBSTACLE or cur == GUARD:
            return False
        self.__obs_row = row
        self.__obs_col = col
        self.__obs_orig = self.grid[row][col]
        self.grid[row][col] = OBSTACLE
        return True

    def __turn(self):
        self.guard_dir = RIGHT if self.guard_dir == UP \
            else DOWN if self.guard_dir == RIGHT \
            else LEFT if self.guard_dir == DOWN \
            else UP

    def __get_next_step(self):
        (dr, dc) = (-1, 0) if self.guard_dir == UP \
            else (1, 0) if self.guard_dir == DOWN \
            else (0, -1) if self.guard_dir == LEFT \
            else (0, 1)
        row, col = self.guard_row + dr, self.guard_col + dc
        if row < 0 \
            or col < 0 \
            or row >= len(self.grid) \
            or col >= len(self.grid[row]):
            return VOID, row, col
        return self.grid[row][col], row, col


p1, p2 = 0, 0
grid = []
with open("input.txt") as f:
    for line in f:
        grid.append(list(line.strip()))
grid = Grid(grid)
while grid.move() != EXITED:
    pass
seen = grid.get_seen_coords()
p1 = len(seen)
grid.reset()

for (row, col) in tqdm(seen):
    if grid.set_obstacle(row, col):
        status = grid.move()
        while status == CONTINUE:
            status = grid.move()
        if status == LOOP:
            p2 += 1
        grid.reset()

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
