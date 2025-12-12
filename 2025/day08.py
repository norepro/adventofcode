#!/usr/bin/python3

from math import dist


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.set_counts = [1] * n
        self.count = n

    def find(self, i):
        if self.parent[i] == i:
            return i
        # Point directly at root
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.set_counts[root_i] < self.set_counts[root_j]:
                self.parent[root_i] = root_j
                self.set_counts[root_j] += self.set_counts[root_i]
            else:
                self.parent[root_j] = root_i
                self.set_counts[root_i] += self.set_counts[root_j]
            self.count -= 1


class Solution:
    def __init__(self, path: str, n_pairs: int):
        with open(path) as f:
            self.coords = [tuple(map(int, x.split(","))) for x in f.readlines()]
            self.i_map = {x: i for i, x in enumerate(self.coords)}
            self.n_pairs = n_pairs

    def run(self):
        p1, p2 = 1, 0
        distances = self.get_distances()
        u = UnionFind(len(self.coords))
        for i in range(len(distances)):
            _, a, b = distances[i]
            ai = self.i_map[a]
            bi = self.i_map[b]
            u.union(ai, bi)
            if i == self.n_pairs - 1:
                for r in list(sorted(u.set_counts, reverse=True))[:3]:
                    p1 *= r
            if u.count == 1:
                p2 = a[0] * b[0]
                break
        return p1, p2

    def get_distances(self):
        distances = []
        for i in range(len(self.coords)):
            a = self.coords[i]
            for j in range(i + 1, len(self.coords)):
                b = self.coords[j]
                d = dist(a, b)
                distances.append((d, a, b))
        distances.sort()
        return distances


def main():
    # solution = Solution("sample.txt", 10)
    solution = Solution("input.txt", 1000)
    return solution.run()


if __name__ == "__main__":
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
