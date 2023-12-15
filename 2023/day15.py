#!/usr/bin/python3

import re


def get_hash(text):
    h = 0
    for c in text:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def put_into_boxes(labels):
    boxes = [[] for _ in range(256)]
    for label in labels:
        m = re.match(r"(.+)([=-])(\d)?", label)
        name, op, focal_len = m.groups()
        box_idx = get_hash(name)
        if op == "=":
            focal_len = int(focal_len)
            for i in range(len(boxes[box_idx])):
                if boxes[box_idx][i][0] == name:
                    boxes[box_idx][i] = (name, focal_len)
                    break
            else:
                boxes[box_idx].append((name, focal_len))
        else:
            for i in range(len(boxes[box_idx])):
                if boxes[box_idx][i][0] == name:
                    del boxes[box_idx][i]
                    break
    return boxes


with open("input.txt", "r") as f:
    labels = f.readline().rstrip().split(",")

boxes = put_into_boxes(labels)
power = 0
for i in range(len(boxes)):
    for j in range(len(boxes[i])):
        power += (1 + i) * (1 + j) * boxes[i][j][1]

print(f"Part 1: {sum([get_hash(s) for s in labels])}")
print(f"Part 2: {power}")
