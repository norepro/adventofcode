#!/usr/bin/python3


def get_empty_rows_cols(image):
    empty_rows = set(range(len(image)))
    empty_cols = set(range(len(image[0])))
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] == "#":
                empty_rows.discard(i)
                empty_cols.discard(j)
    return (empty_rows, empty_cols)


def get_ids(image):
    ids = {}
    id = 1
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] == "#":
                ids[id] = (i, j)
                id += 1
    return ids


def get_shortest_paths(ids, empty_rows, empty_cols, expansion=1_000_000):
    paths = {}
    max_id = max(ids.keys())
    for i in range(1, max_id + 1):
        for j in range(i + 1, max_id + 1):
            dx = abs(ids[j][1] - ids[i][1])
            dy = abs(ids[j][0] - ids[i][0])
            for x in empty_cols:
                if min(ids[i][1], ids[j][1]) <= x <= max(ids[i][1], ids[j][1]):
                    dx += expansion - 1
            for y in empty_rows:
                if min(ids[i][0], ids[j][0]) <= y <= max(ids[i][0], ids[j][0]):
                    dy += expansion - 1
            paths[(i, j)] = dx + dy
    return paths


image = []
with open("input.txt", "r") as f:
    for line in f:
        image.append(list(line.strip()))
empty_rows, empty_cols = get_empty_rows_cols(image)
ids = get_ids(image)
print(f"Part 1: {sum(get_shortest_paths(ids, empty_rows, empty_cols, 2).values())}")
print(f"Part 2: {sum(get_shortest_paths(ids, empty_rows, empty_cols).values())}")
