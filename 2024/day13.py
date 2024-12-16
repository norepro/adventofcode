#!/usr/bin/python3

import re


class Machine:

    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize

    def get_presses(self):
        xa, ya = self.a
        xb, yb = self.b
        xp, yp = self.prize
        a = (yb * xp - xb * yp) / (yb * xa - ya * xb)
        b = (yp - a * ya) / yb
        return (a, b)


machines = []
with open("input.txt") as f:
    for line in f:
        m = re.search(r'(Button [AB]|Prize): X.(\d+), Y.(\d+)', line)
        if m:
            xy = (int(m.group(2)), int(m.group(3)))
            if m.group(1).startswith('B'):
                if m.group(1).endswith('A'):
                    a = xy
                else:
                    b = xy
            else:
                machines.append(Machine(a, b, xy))

PART2_DELTA = 10000000000000
p1, p2 = 0, 0
for m in machines:
    a, b = m.get_presses()
    if a.is_integer() and b.is_integer():
        p1 += int(3 * a + b)
    m.prize = (m.prize[0] + PART2_DELTA, m.prize[1] + PART2_DELTA)
    a, b = m.get_presses()
    if a.is_integer() and b.is_integer():
        p2 += int(3 * a + b)
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
