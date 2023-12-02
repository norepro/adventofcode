#!/usr/bin/python3

import re


def to_num(s):
    return int(name_to_num[s] if len(s) > 1 else s)


totals = [0, 0]
name_to_num = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

rx = [r"(\d)", r"(?=(\d|" + "|".join(name_to_num) + "))"]

with open("input.txt", "r") as f:
    for line in f:
        for i in range(len(totals)):
            m = re.findall(rx[i], line)
            if len(m) == 0:
                continue
            totals[i] += to_num(m[0]) * 10 + to_num(m[-1])
print(f"Part 1: {totals[0]}")
print(f"Part 2: {totals[1]}")
