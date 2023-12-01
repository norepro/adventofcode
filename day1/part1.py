import re

total = 0


with open("input.txt", "r") as f:
    for line in f:
        m = re.findall(r"(\d)", line)
        if len(m) == 0:
            continue
        total += int(m[0]) * 10 + int(m[-1])
print(total)
