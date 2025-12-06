#!/usr/bin/python3

from collections import defaultdict, deque


class Solution:
    def __init__(self, path: str):
        self.rolls: set[tuple[int, int]] = set()
        self.neighbor_count: dict[tuple[int, int], int] = {}
        self.neighbors: defaultdict[tuple[int, int], list[tuple[int, int]]] = (
            defaultdict(list)
        )
        self.n_rows = 0
        self.n_cols = 0
        with open(path) as f:
            col = 0
            for line in f:
                for col, c in enumerate(line):
                    if c == "@":
                        self.rolls.add((self.n_rows, col))
                self.n_rows += 1
                self.n_cols = max(self.n_cols, col)

    def run(self):
        candidates = self.get_initial_removal_candidates()
        initial_movable_count = len(candidates)
        total_movable_count = self.remove_movable(candidates)
        return initial_movable_count, total_movable_count

    def get_right_down_neighbors(self, row: int, col: int):
        if col + 1 < self.n_cols:
            if row > 0:
                yield (row - 1, col + 1)
            yield (row, col + 1)
            if row + 1 < self.n_rows:
                yield (row + 1, col + 1)
        if row + 1 < self.n_rows:
            yield (row + 1, col)

    def remove_movable(self, candidates: deque[tuple[int, int]]):
        remove_count = 0
        while candidates:
            roll = candidates.pop()
            if roll in self.rolls:
                for n in self.neighbors[roll]:
                    if n in self.rolls:
                        self.neighbor_count[n] -= 1
                        if 0 <= self.neighbor_count[n] < 4:
                            candidates.append(n)
                self.rolls.remove(roll)
                remove_count += 1
        return remove_count

    def get_initial_removal_candidates(self):
        candidates: deque[tuple[int, int]] = deque()
        for roll in self.rolls:
            neighbors = self.neighbors[roll]
            for n in self.get_right_down_neighbors(*roll):
                if n in self.rolls:
                    neighbors.append(n)
                    self.neighbors[n].append(roll)
        for roll in self.rolls:
            n_len = len(self.neighbors[roll])
            self.neighbor_count[roll] = n_len
            if n_len < 4:
                candidates.append(roll)
        return candidates


def main():
    solution = Solution("input.txt")
    return solution.run()


if __name__ == "__main__":
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
