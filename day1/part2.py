import re

total = 0
map = {
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


def to_num(s):
    return int(map[s] if len(s) > 1 else s)


with open("input.txt", "r") as f:
    for line in f:
        m = re.findall(
            r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line
        )
        if len(m) == 0:
            continue
        total += to_num(m[0]) * 10 + to_num(m[-1])
print(total)
