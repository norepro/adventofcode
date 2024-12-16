#!/usr/bin/python3

from tqdm import tqdm


class Box:

    def __init__(self, pos):
        self.pos = pos

    def update(self, pos):
        self.pos = pos

    def __repr__(self) -> str:
        return f"Box({self.pos})"


class Grid:

    def __init__(self, grid, is_wide=False):
        m = 2 if is_wide else 1
        self.is_wide = is_wide
        self.grid = [['.'] * len(x) * m for x in grid]
        self.boxes = []
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                if col == '@':
                    self.robot = (r, c * m)
                elif col == 'O':
                    self.boxes.append(Box((r, c * m)))
                elif col == '#':
                    self.grid[r][c * m] = '#'
                    if is_wide:
                        self.grid[r][c * m + 1] = '#'

    def print(self, limit_rows=False):
        bs = list(sorted(self.boxes, key=lambda b: b.pos))
        if limit_rows:
            bs = [
                b for b in bs
                if self.robot[0] - 3 <= b.pos[0] <= self.robot[0] + 3
            ]
        print()
        for r, row in enumerate(self.grid):
            if limit_rows and (r < self.robot[0] - 3 or r > self.robot[0] + 3):
                continue
            c = 0
            while c < len(row):
                if row[c] == '#':
                    print('#', end='')
                    c += 1
                    continue
                p = (r, c)
                if self.robot == p:
                    print('@', end='')
                    c += 1
                elif len(bs) > 0 and bs[0].pos[0] == r and bs[0].pos[1] == c:
                    del bs[0]
                    c += 1
                    if self.is_wide:
                        print('[]', end='')
                        c += 1
                    else:
                        print('O', end='')
                else:
                    print('.', end='')
                    c += 1
            print()

    def move(self, dir):
        v = self._get_dir_vector(dir)
        boxes = self._get_boxes_to_move(v)
        for box in boxes:
            box.update((box.pos[0] + v[0], box.pos[1] + v[1]))
        rp = (self.robot[0] + v[0], self.robot[1] + v[1])
        if self.grid[rp[0]][rp[1]] != '#' and not self._get_box_at(rp):
            self.robot = rp

    def gps_sum(self):
        return sum([100 * b.pos[0] + b.pos[1] for b in self.boxes])

    def _get_box_at(self, pos):
        for box in self.boxes:
            if (self.is_wide and box.pos[0] == pos[0] and
                (pos[1] == box.pos[1]
                 or pos[1] == box.pos[1] + 1)) or box.pos == pos:
                return box
        return None

    def _get_dir_vector(self, dir):
        return (-1, 0) if dir == '^' \
            else (1, 0) if dir == 'v' \
            else (0, -1) if dir == '<' \
            else (0, 1)

    def _get_boxes_to_move(self, v):
        to_move = []
        to_check = [(self.robot[0] + v[0], self.robot[1] + v[1])]
        checked = set()
        to_move_dedupe = set()
        while len(to_check) > 0:
            tc = to_check.pop()
            if self.grid[tc[0]][tc[1]] == '#':
                to_move.clear()
                break
            if tc in checked:
                continue
            checked.add(tc)
            box = self._get_box_at(tc)
            if box:
                if box.pos not in to_move_dedupe:
                    to_move.append(box)
                    to_move_dedupe.add(box.pos)
                if not self.is_wide:
                    to_check.append((box.pos[0] + v[0], box.pos[1] + v[1]))
                elif v[1] == -1:
                    to_check.append((box.pos[0] + v[0], box.pos[1] + v[1]))
                elif v[1] == 1:
                    to_check.append((box.pos[0] + v[0], box.pos[1] + v[1] + 1))
                else:
                    to_check.append((box.pos[0] + v[0], box.pos[1] + v[1]))
                    to_check.append((box.pos[0] + v[0], box.pos[1] + v[1] + 1))
        return to_move


with open("input.txt") as f:
    data = f.read().split('\n\n')
original_grid = [list(x) for x in data[0].split('\n')]
grid = Grid(original_grid)
moves = list(data[1].replace('\n', ''))
for m in tqdm(moves):
    grid.move(m)
print(f"Part 1: {grid.gps_sum()}")

grid = Grid(original_grid, True)
for m in tqdm(moves):
    grid.move(m)
print(f"Part 2: {grid.gps_sum()}")
