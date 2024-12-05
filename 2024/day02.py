#!/usr/bin/python3


def is_safe(d):
    diffs = [d[i] - d[i - 1] for i in range(1, len(d))]
    for i in range(len(diffs)):
        dcurr = diffs[i]
        if abs(dcurr) < 1 or abs(dcurr) > 3:
            return False
        if i > 0:
            dprev = diffs[i - 1]
            if (dcurr > 0 and dprev < 0) or (dcurr < 0 and dprev > 0):
                return False
    return True


safe_count, safe_dampened_count = 0, 0
with open("input.txt") as f:
    for line in f:
        d = list(map(int, line.split()))
        if is_safe(d):
            safe_count += 1
            safe_dampened_count += 1
            continue
        for i in range(len(d)):
            d_dampened = [x for idx, x in enumerate(d) if idx != i]
            if is_safe(d_dampened):
                safe_dampened_count += 1
                break

print(f"Part 1: {safe_count}")
print(f"Part 2: {safe_dampened_count}")
