#!/usr/bin/python3


class Solution:

    def __init__(self, path: str):
        with open(path) as f:
            ranges, ids = f.read().split("\n\n")
        self.ranges = [
            list(map(int, x.split('-'))) for x in ranges.split('\n')
        ]
        self.ranges.sort()
        self.ids = [int(x) for x in ids.rstrip().split('\n')]
        self.ids.sort()
        self._merge_ranges()

    def run(self):
        valid_count = 0
        all_valid_count = 0

        # Both ranges and ids are sorted. Create indices into both and
        # increment either depending which one is lower.
        id_i, range_i = 0, 0
        while id_i < len(self.ids) and range_i < len(self.ranges):
            id = self.ids[id_i]
            range_ = self.ranges[range_i]
            if id < range_[0]:
                # id is lower, check next one
                id_i += 1
            elif range_[0] <= id <= range_[1]:
                # id is valid
                valid_count += 1
                id_i += 1
            else:
                # id is greater than the range, try next range
                all_valid_count += range_[1] - range_[0] + 1
                range_i += 1
        # Sum up any remaining ranges after ids are exhausted
        for range_i in range(range_i, len(self.ranges)):
            range_ = self.ranges[range_i]
            all_valid_count += range_[1] - range_[0] + 1
        return valid_count, all_valid_count

    def _merge_ranges(self):
        for i in range(len(self.ranges) - 1, 0, -1):
            curr = self.ranges[i]
            prev = self.ranges[i - 1]
            if prev[0] <= curr[0] <= prev[1]:
                prev[1] = max(curr[1], prev[1])
                del self.ranges[i]


def main():
    solution = Solution('input.txt')
    return solution.run()


if __name__ == '__main__':
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
