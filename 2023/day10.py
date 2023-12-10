#!/usr/bin/python3

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

dirs = {
    "|": [True, False, True, False],
    "-": [False, True, False, True],
    "L": [True, True, False, False],
    "J": [True, False, False, True],
    "7": [False, False, True, True],
    "F": [False, True, True, False],
    ".": [False, False, False, False],
}


def dirs_with_vector(v):
    return [k for k in dirs if dirs[k][v]]


def get_pipe_type(grid, row, col):
    types = set(dirs.keys())
    if col > 0 and dirs[grid[row][col - 1]][RIGHT]:
        types = types.intersection(set(dirs_with_vector(LEFT)))
    if col < len(grid[row]) - 1 and dirs[grid[row][col + 1]][LEFT]:
        types = types.intersection(set(dirs_with_vector(RIGHT)))
    if row > 0 and dirs[grid[row - 1][col]][DOWN]:
        types = types.intersection(set(dirs_with_vector(UP)))
    if row < len(grid) - 1 and dirs[grid[row + 1][col]][UP]:
        types = types.intersection(set(dirs_with_vector(DOWN)))
    return next(iter(types))


def get_next_dir(d, avoid=-1):
    urdl = dirs[d]
    for i in range(len(urdl)):
        if urdl[i] and i != avoid:
            return i


def get_step_count(grid, row, col, visited):
    count = 0
    r, c = row, col
    prev_dir = get_next_dir(grid[row][col])
    while count == 0 or r != row or c != col:
        visited[r][c] = grid[r][c]
        next_dir = get_next_dir(grid[r][c], prev_dir)
        if next_dir == UP:
            r -= 1
        elif next_dir == RIGHT:
            c += 1
        elif next_dir == DOWN:
            r += 1
        else:
            c -= 1
        count += 1
        prev_dir = (next_dir + 2) % 4
    return count


def get_previous_turn(grid, row, col):
    for i in range(col - 1, -1, -1):
        pipe = grid[row][i]
        match pipe:
            case "L" | "F":
                return pipe
            case _:
                pass
    return None


def count_contained(grid):
    count = 0
    for i in range(len(grid)):
        inside = False
        for j in range(len(grid[i])):
            pipe = grid[i][j]
            match pipe:
                case "|" | "L" | "F":
                    inside = not inside
                case "J":
                    if not get_previous_turn(grid, i, j) == "F":
                        inside = not inside
                case "7":
                    if not get_previous_turn(grid, i, j) == "L":
                        inside = not inside
                case ".":
                    if inside:
                        count += 1
                    else:
                        grid[i][j] = "O"
                case _:
                    pass
    return count


def print_grid(grid):
    t = str.maketrans("|-LJ7F", "\u2502\u2500\u2514\u2518\u2510\u250C")
    for row in grid:
        print("".join(row).translate(t))


grid = []
visited = []
sr, sc = -1, -1
with open("input.txt", "r") as f:
    for line in f:
        grid.append(line.strip())
        visited.append(["."] * len(grid[-1]))
        if sc == -1:
            sc = line.find("S")
            sr += 1
grid[sr] = grid[sr].replace("S", get_pipe_type(grid, sr, sc))
steps = get_step_count(grid, sr, sc, visited)
print(f"Part 1: {int(steps / 2)}")
print(f"Part 2: {count_contained(visited)}")
