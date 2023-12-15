#!/usr/bin/python3


def get_reflection(pattern, exclude=None):
    pr = set(range(1, len(pattern)))
    pc = set(range(1, len(pattern[0])))
    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            # Vertical reflections
            n = min(col, len(pattern[row]) - col)
            for i in range(n):
                if pattern[row][col - 1 - i] != pattern[row][col + i]:
                    pc.discard(col)
                    break
            # Horizontal reflections
            n = min(row, len(pattern) - row)
            for i in range(n):
                if pattern[row - 1 - i][col] != pattern[row + i][col]:
                    pr.discard(row)
                    break
    if exclude:
        if exclude[0]:
            pc.discard(exclude[1])
        else:
            pr.discard(exclude[1])
    if len(pr) ^ len(pc) == 1:
        return (False, next(iter(pr))) if len(pr) == 1 else (True, next(iter(pc)))
    return None


def score_reflection(reflection):
    return reflection[1] if reflection[0] else reflection[1] * 100


patterns = []
pattern = None
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        if len(line) > 0:
            if not pattern:
                pattern = []
            pattern.append(line)
        else:
            patterns.append(pattern)
            pattern = None
    if pattern:
        patterns.append(pattern)
total = sum([score_reflection(get_reflection(p)) for p in patterns])
print(f"Part 1: {total}")

total = 0
for pattern in patterns:
    orig_reflect = get_reflection(pattern)
    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            d = pattern[row]
            c = "#" if pattern[row][col] == "." else "."
            pattern[row] = d[:col] + c + d[col + 1 :]
            r = get_reflection(pattern, orig_reflect)
            pattern[row] = d
            if r:
                total += r[1] if r[0] else r[1] * 100
                break
        else:
            continue
        break
print(f"Part 2: {total}")
