#!/usr/bin/python3


def get_next_element(seq):
    if all(map(lambda x: x == 0, seq)):
        return 0
    diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    return seq[-1] + get_next_element(diffs)


part1_total = 0
part2_total = 0
with open("input.txt", "r") as f:
    for line in f:
        seq = list(map(int, line.split()))
        part1_total += get_next_element(seq)
        seq.reverse()
        part2_total += get_next_element(seq)

print(f"Part 1: {part1_total}")
print(f"Part 2: {part2_total}")
