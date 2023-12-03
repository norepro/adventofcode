#!/usr/bin/python3

max_totals = [0, 0, 0]

with open("input.txt", "r") as f:
    elf_total = 0
    for line in f:
        if line.strip():
            elf_total += int(line)
        else:
            max_totals.append(elf_total)
            max_totals = list(sorted(max_totals))[1:]
            elf_total = 0
print(f"Part 1: {max_totals[0]}")
print(f"Part 2: {sum(max_totals)}")
