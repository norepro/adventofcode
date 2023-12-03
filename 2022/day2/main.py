#!/usr/bin/python3

ROCK = 1
PAPER = 2
SCISSORS = 3
COMPARE = [SCISSORS, ROCK, PAPER, SCISSORS, ROCK]

part1_score = 0
part2_score = 0


def get_score(them, us):
    we_won = us == COMPARE[them + 1]
    return us + (6 if we_won else (3 if us == them else 0))


def adjust_move(them, us):
    if us == 1:
        return COMPARE[them - 1]
    elif us == 2:
        return them
    else:
        return COMPARE[them + 1]


with open("input.txt", "r") as f:
    for line in f:
        if len(line) >= 3:
            them, us = (ord(line[0]) - 64, ord(line[2]) - 87)
            part1_score += get_score(them, us)
            us = adjust_move(them, us)
            part2_score += get_score(them, us)

print(f"Part 1: {part1_score}")
print(f"Part 2: {part2_score}")
