#!/usr/bin/python3

n = 50
num_exact_zero = 0
num_clicked_zero = 0
with open("input.txt") as f:
    for line in f:
        (direction, distance) = (line[0], int(line[1:]))
        num_clicked_zero += distance // 100
        distance %= 100
        if direction == "L":
            if n > 0 and distance > n:
                num_clicked_zero += 1
            distance *= -1
        elif n + distance > 100:
            num_clicked_zero += 1
        n += distance
        n %= 100
        if n == 0:
            num_exact_zero += 1
            num_clicked_zero += 1
print(f"Part 1: {num_exact_zero}")
print(f"Part 2: {num_clicked_zero}")
