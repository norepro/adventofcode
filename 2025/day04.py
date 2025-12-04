#!/usr/bin/python3

from collections import deque


class Solution:

    def __init__(self, path: str):
        self.rolls = set()
        self.neighbor_count = {}
        self.n_rows = 0
        self.n_cols = 0
        with open(path) as f:
            for line in f:
                for col, c in enumerate(line):
                    if c == '@':
                        self.rolls.add((self.n_rows, col))
                self.n_rows += 1
                self.n_cols = max(self.n_cols, col)

    def run(self):
        initial_movable_count = self.remove_movable()
        total_movable_count = initial_movable_count
        last_removed = initial_movable_count
        while last_removed > 0:
            last_removed = self.remove_movable()
            total_movable_count += last_removed
        return initial_movable_count, total_movable_count

    def get_neighbors(self, row: int, col: int):
        for r in range(max(0, row - 1), min(self.n_rows, row + 2)):
            for c in range(max(0, col - 1), min(self.n_cols, col + 2)):
                if r != row or c != col:
                    yield (r, c)

    def count_surrounding(self, row: int, col: int):
        count = 0
        for r, c in self.get_neighbors(row, col):
            if (r, c) in self.rolls:
                count += 1
        return count

    def remove_movable(self):
        to_remove = deque(maxlen=len(self.rolls))
        for roll in self.rolls:
            count = self.neighbor_count.get(roll, -1)
            if count == -1:
                count = self.count_surrounding(roll[0], roll[1])
                self.neighbor_count[roll] = count
            if count < 4:
                to_remove.append(roll)
        for roll in to_remove:
            self.rolls.remove(roll)
            for n in self.get_neighbors(roll[0], roll[1]):
                if n in self.neighbor_count:
                    self.neighbor_count[n] -= 1
        return len(to_remove)


def main():
    solution = Solution('input.txt')
    return solution.run()


if __name__ == '__main__':
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
