#!/usr/bin/python3


def is_word(word, grid, row, col, dr, dc):
    if row < 0 or \
        row >= len(grid) or \
        col < 0 or \
        col >= len(grid[row]) or \
        (dc > 0 and col > len(grid[row]) - len(word)) or \
        (dc < 0 and col < len(word) - 1) or \
        (dr > 0 and row > len(grid) - len(word)) or \
        (dr < 0 and row < len(word) - 1):
        return False
    for i in range(len(word)):
        if grid[row + i * dr][col + i * dc] != word[i]:
            return False
    return True


p1, p2 = 0, 0
grid = []
with open("input.txt") as f:
    for line in f:
        grid.append(list(line.strip()))
for row in range(len(grid)):
    for col in range(len(grid[row])):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if is_word('XMAS', grid, row, col, dr, dc):
                    p1 += 1
        if grid[row][col] != 'A':
            continue
        down_right = is_word('MAS', grid, row - 1, col - 1, 1, 1) or \
            is_word('MAS', grid, row + 1, col + 1, -1, -1)
        up_right = is_word('MAS', grid, row + 1, col - 1, -1, 1) or \
            is_word('MAS', grid, row - 1, col + 1, 1, -1)
        if down_right and up_right:
            p2 += 1

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
