#!/usr/bin/python3

DIRS = ["R", "D", "L", "U"]


def get_coords(steps):
    coords = []
    x = y = 0
    for step in steps:
        n = step[1]
        match step[0]:
            case "R":
                x += n
            case "L":
                x -= n
            case "U":
                y += n
            case "D":
                y -= n
        coords.append((x, y))
    return coords


def determinant(a, b):
    return a[0] * b[1] - a[1] * b[0]


def shoelace_area(coords):
    # https://en.wikipedia.org/wiki/Shoelace_formula
    area = 0
    for i in range(1, len(coords)):
        area += determinant(coords[i - 1], coords[i])
    area += determinant(coords[-1], coords[0])
    return abs(area / 2)


def get_area(steps):
    coords = get_coords(steps)
    shoelace = int(shoelace_area(coords))
    perimeter = sum([s[1] for s in steps])

    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    #
    # Theorem: A = i + b/2 - 1
    # A is shoelace area above which does not account for boundary points.
    # AOC problem is asking us for the sum of boundary points plus internal,
    # represented by 'i' and 'b' in theorem above. Refactoring:
    #
    # i = A - b/2 + 1
    # i + b = A + b/2 + 1
    return shoelace + perimeter // 2 + 1


def hex_to_step(h):
    # (#70c710)
    return (DIRS[int(h[-2:-1])], int(h[2:-2], 16))


steps = []
with open("input.txt", "r") as f:
    for line in f:
        dir, n, color = line.rstrip().split()
        steps.append((dir, int(n), color))

print(f"Part 1: {get_area(steps)}")

steps = [hex_to_step(s[2]) for s in steps]
print(f"Part 2: {get_area(steps)}")
