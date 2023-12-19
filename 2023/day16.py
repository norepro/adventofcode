#!/usr/bin/python3

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

DIR_LAMBDAS = [
    (LEFT, lambda r, c: (r, c - 1)),
    (RIGHT, lambda r, c: (r, c + 1)),
    (UP, lambda r, c: (r - 1, c)),
    (DOWN, lambda r, c: (r + 1, c)),
]

DIR_MAP = {
    ".": DIR_LAMBDAS,
    "/": [
        DIR_LAMBDAS[DOWN],
        DIR_LAMBDAS[UP],
        DIR_LAMBDAS[RIGHT],
        DIR_LAMBDAS[LEFT],
    ],
    "\\": [
        DIR_LAMBDAS[UP],
        DIR_LAMBDAS[DOWN],
        DIR_LAMBDAS[LEFT],
        DIR_LAMBDAS[RIGHT],
    ],
}


def traverse_grid(grid, row=0, col=0, direction=RIGHT):
    if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[row]):
        return
    cell = grid[row][col]
    while not cell[1 + direction]:
        cell[1 + direction] = True
        match cell[0]:
            case "." | "/" | "\\":
                rcl = DIR_MAP[cell[0]][direction]
                direction = rcl[0]
                row, col = rcl[1](row, col)
            case "-":
                if direction == UP or direction == DOWN:
                    traverse_grid(grid, row, col - 1, LEFT)
                    traverse_grid(grid, row, col + 1, RIGHT)
                    break
                else:
                    row, col = DIR_LAMBDAS[direction][1](row, col)
            case "|":
                if direction == LEFT or direction == RIGHT:
                    traverse_grid(grid, row - 1, col, UP)
                    traverse_grid(grid, row + 1, col, DOWN)
                    break
                else:
                    row, col = DIR_LAMBDAS[direction][1](row, col)
        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[row]):
            return
        cell = grid[row][col]


def count_energized_tiles(grid):
    total = 0
    for row in grid:
        for col in row:
            if col[1] or col[2] or col[3] or col[4]:
                total += 1
    return total


def reset_grid(grid):
    for row in grid:
        for col in row:
            col[1] = False
            col[2] = False
            col[3] = False
            col[4] = False


grid = []
with open("input.txt", "r") as f:
    for line in f:
        grid.append([[c, False, False, False, False] for c in line.rstrip()])
traverse_grid(grid)
print(f"Part 1: {count_energized_tiles(grid)}")

max_energized = 0
for row in range(len(grid)):
    reset_grid(grid)
    traverse_grid(grid, row, 0, RIGHT)
    max_energized = max(max_energized, count_energized_tiles(grid))
    reset_grid(grid)
    traverse_grid(grid, row, len(grid[row]) - 1, LEFT)
    max_energized = max(max_energized, count_energized_tiles(grid))
for col in range(len(grid[0])):
    reset_grid(grid)
    traverse_grid(grid, 0, col, DOWN)
    max_energized = max(max_energized, count_energized_tiles(grid))
    reset_grid(grid)
    traverse_grid(grid, len(grid) - 1, col, UP)
    max_energized = max(max_energized, count_energized_tiles(grid))
print(f"Part 2: {max_energized}")
