#!/usr/bin/python3

from tqdm import tqdm


class Rule:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_applicable(self, pages):
        seen_x, seen_y = False, False
        for page in pages:
            if page == self.x:
                seen_x = True
            elif page == self.y:
                seen_y = True
        return seen_x and seen_y

    def is_correct_order(self, pages):
        seen_x, seen_y = False, False
        for page in pages:
            if page == self.x:
                if seen_y:
                    return False
                seen_x = True
            elif page == self.y:
                if seen_x:
                    return True
                seen_y = True
        return True


def get_middle(d):
    return d[int(len(d) / 2)]


def make_correct(update, rules):
    rules = [r for r in rules if r.is_applicable(update)]
    while True:
        for rule in rules:
            if not rule.is_correct_order(update):
                xi = update.index(rule.x)
                yi = update.index(rule.y)
                update[xi], update[yi] = update[yi], update[xi]
                break
        else:
            break


p1, p2 = 0, 0
rules, updates = [], []
with open("input.txt") as f:
    for line in f:
        if '|' in line:
            (x, y) = (map(int, line.split('|')))
            rules.append(Rule(x, y))
        if ',' in line:
            updates.append(list(map(int, line.split(','))))
for update in tqdm(updates):
    for rule in rules:
        if not rule.is_correct_order(update):
            make_correct(update, rules)
            p2 += get_middle(update)
            break
    else:
        p1 += get_middle(update)

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
