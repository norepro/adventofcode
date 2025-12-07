#!/usr/bin/python3

from functools import cache


class Solution:
    def __init__(self, path: str):
        with open(path) as f:
            self.start = f.readline().index("S")
            self.rows = []
            for line in f:
                row = []
                for i in range(len(line)):
                    if line[i] == "^":
                        row.append(i)
                if row:
                    self.rows.append(row)

    def run(self):
        first = self.normal_split()
        second = self.many_worlds(self.start, 0)
        return first, second

    def normal_split(self):
        split_count = 0
        beams = set()
        beams.add(self.start)
        for row in self.rows:
            to_add = []
            for col in row:
                if col in beams:
                    split_count += 1
                    to_add.append(col)
                    beams.remove(col)
            for col in to_add:
                beams.add(col - 1)
                beams.add(col + 1)
        return split_count

    @cache
    def many_worlds(self, beam_loc, row_idx):
        if row_idx == len(self.rows):
            return 1
        next_row = row_idx + 1
        if beam_loc in self.rows[row_idx]:
            return self.many_worlds(beam_loc - 1, next_row) + self.many_worlds(
                beam_loc + 1, next_row
            )
        else:
            return self.many_worlds(beam_loc, next_row)


def main():
    solution = Solution("input.txt")
    return solution.run()


if __name__ == "__main__":
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
