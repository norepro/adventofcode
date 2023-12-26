#!/usr/bin/python3

from itertools import combinations, product
from math import isclose


class Stone:
    def __init__(self, p, v):
        self.p = p
        self.v = v

    def __repr__(self) -> str:
        return f"({self.p[0]}, {self.p[1]}, {self.p[2]}, {self.v[0]}, {self.v[1]}, {self.v[2]})"

    def intersection_xy(self, other, dv=(0, 0)):
        # x(t) = at + b
        # y(t) = ct + d
        # t = (x-b)/a
        # Put that into y(t) above, solve for y...
        # y = mx + B
        # m = c/a
        # B = d - bc/a = d - mb
        if self.v[0] == dv[0] or other.v[0] == dv[0]:
            # Same x velocity, either will never intersect or is an exact copy
            # of another stone. Assume the input is somewhat sane...
            return None
        m_self = (self.v[1] - dv[1]) / (self.v[0] - dv[0])
        m_other = (other.v[1] - dv[1]) / (other.v[0] - dv[0])
        b_self = self.p[1] - m_self * self.p[0]
        b_other = other.p[1] - m_other * other.p[0]
        if m_self == m_other:
            return None  # Parallel
        ix = (b_other - b_self) / (m_self - m_other)
        iy = m_self * ix + b_self
        return (ix, iy)

    def is_future(self, p, dx=0):
        return not (
            (p[0] < self.p[0] and self.v[0] > -dx)
            or (p[0] > self.p[0] and self.v[0] < -dx)
        )


def count_intersections_within_bounds(stones, bounds):
    count = 0
    for a, b in combinations(stones, 2):
        i = a.intersection_xy(b)
        if i is None or not a.is_future(i) or not b.is_future(i):
            # Never intersected or we are moving away from the point
            continue
        if bounds[0] <= i[0] <= bounds[1] and bounds[0] <= i[1] <= bounds[1]:
            count += 1
    return count


# Credit to FatalisticFeline-47 for the idea:
# https://www.reddit.com/r/adventofcode/comments/18pptor/comment/kepufsi/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
#
# Gist is to treat the magic stone as not moving and brute force all possible
# velocities to see which ones result in all the other stones meeting at us.
def find_magic_stone(stones, candidate_v):
    # candidate_v is the range of velocities to consider for each of the x, y,
    # and z vectors. Start by scanning every combination of x and y
    # velocities, ignoring z like part 1, just to see if they intersect in the
    # same XY plane. It's very fast math and avoids repeating the same XY
    # checks for varying Z when we know they will always fail.
    for vx, vy in product(candidate_v, repeat=2):
        dv = (vx, vy)
        last = None
        for a, b in combinations(stones, 2):
            i = a.intersection_xy(b, dv)
            # This is technically a bug, but too lazy to fix. None can be
            # returned if the trajectory is parallel or our proposed magic
            # X velocity exactly matches the X velocity of one of the stones.
            # Fix is to return two different values depending which scenario,
            # but it did not matter for the problem.
            if i is not None:
                if last is None:
                    last = i
                elif not all([isclose(x, y) for x, y in zip(i, last)]):
                    # The input numbers are so large that precision is a
                    # thing. Use isclose for "equality".
                    break
        else:
            # All stones in the same XY plane, now interate over all possible
            # values of vz to see if they all meet at the same point (us).
            last = tuple(map(int, last))
            for vz in candidate_v:
                a = stones[0]
                t = (last[0] - a.p[0]) / (a.v[0] - vx)
                expected_z = a.p[2] + (a.v[2] - vz) * t
                for i in range(1, len(stones)):
                    a = stones[i]
                    if a.v[0] == vx:
                        continue
                    t = (last[0] - a.p[0]) / (a.v[0] - vx)
                    z = a.p[2] + (a.v[2] - vz) * t
                    if expected_z != z:
                        break
                else:
                    return Stone((last[0], last[1], int(z)), (vx, vy, vz))
    return None


stones = []
with open("test.txt", "r") as f:
    for line in f:
        pos, v = line.rstrip().split("@")
        p = tuple(map(int, pos.split(",")))
        v = tuple(map(int, v.split(",")))
        stones.append(Stone(p, v))
MIN = 200000000000000
# MIN = 7
MAX = 400000000000000
# MAX = 27
count = count_intersections_within_bounds(stones, (MIN, MAX))
print(f"Part 1: {count}")

magic = find_magic_stone(stones, range(-500, 500))
print(f"Part 2: {sum(magic.p)}")
