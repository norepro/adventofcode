#!/usr/bin/env python3

from itertools import permutations
from functools import cache


class Keypad:

    def __init__(self, keys):
        self.keys = keys
        self.index = {}
        for r, row in enumerate(keys):
            for c, col in enumerate(row):
                self.index[col] = (r, c)
        self.x = self.index['X']

    def get_path(self, start, end):
        a = self.index[start]
        b = self.index[end]
        ns_dist = abs(a[0] - b[0])
        ns_keys = '^' * ns_dist if a[0] > b[0] else 'v' * ns_dist
        ew_dist = abs(a[1] - b[1])
        ew_keys = '<' * ew_dist if a[1] > b[1] else '>' * ew_dist
        if a[0] == self.x[0]:
            keys = ns_keys + ew_keys
        else:
            keys = ew_keys + ns_keys
        return keys + 'A'

    def is_valid(self, keys, start, end):
        if keys[-1] != 'A':
            return False

        pos = self.index[start]
        for key in keys:
            if key == '<':
                pos = (pos[0], pos[1] - 1)
            elif key == '>':
                pos = (pos[0], pos[1] + 1)
            elif key == 'v':
                pos = (pos[0] + 1, pos[1])
            elif key == '^':
                pos = (pos[0] - 1, pos[1])
            if pos[0] < 0 or pos[0] >= len(self.keys) or \
                pos[1] < 0 or pos[1] >= len(self.keys[0]) or pos == self.x:
                return False
        return True


class NumericKeypad(Keypad):

    def __init__(self):
        Keypad.__init__(self,
                        [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'],
                         ['X', '0', 'A']])


class ArrowKeypad(Keypad):

    def __init__(self):
        Keypad.__init__(self, [['X', '^', 'A'], ['<', 'v', '>']])


@cache
def get_min_presses(code, max_depth, depth=0):
    if depth == max_depth:
        return len(code)
    pad = NumericKeypad() if depth == 0 else ArrowKeypad()
    min_presses = 0
    for i, c in enumerate(code):
        min_for_c = float('inf')
        prev = 'A' if i == 0 else code[i - 1]
        path = pad.get_path(prev, c)
        for p in permutations(path):
            keys = ''.join(p)
            if not pad.is_valid(keys, prev, c):
                continue
            p_presses = get_min_presses(keys, max_depth, depth + 1)
            min_for_c = min(min_for_c, p_presses)
        min_presses += min_for_c
    return min_presses


with open("input.txt") as f:
    codes = [x.rstrip() for x in f]
p1, p2 = 0, 0
for code in codes:
    p1 += get_min_presses(code, 3) * int(code[:-1])
    p2 += get_min_presses(code, 26) * int(code[:-1])
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
