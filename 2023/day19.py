#!/usr/bin/python3

import re
from math import prod


class Rule:
    def __init__(self, rule):
        m = re.match(r"(.)([<>])(\d+):(.+)", rule)
        if m:
            self.field = m.group(1)
            self.op = m.group(2)
            self.value = int(m.group(3))
            self.next = m.group(4)
        else:
            self.op = None
            self.next = rule

    def get_next(self, part):
        if self.op == "<":
            return self.next if part[self.field] < self.value else None
        elif self.op == ">":
            return self.next if part[self.field] > self.value else None
        return self.next


def get_rating_total(workflows, parts):
    rating_total = 0
    for part in parts:
        workflow = "in"
        while workflow != "R" and workflow != "A":
            for rule in workflows[workflow]:
                new_wf = rule.get_next(part)
                if new_wf:
                    workflow = new_wf
                    break
        if workflow == "A":
            rating_total += sum(part.values())
    return rating_total


def split_limits(limits, op, value):
    new_limits = []
    if op == "<":
        for limit in limits:
            if limit[1] < value:
                new_limits.append(limit)
            elif limit[0] < value:
                new_limits.append((limit[0], value - 1))
                break
    else:
        for limit in limits:
            if limit[0] > value:
                new_limits.append(limit)
            elif limit[1] > value:
                new_limits.append((value + 1, limit[1]))
    return new_limits


def sum_limits(limits):
    return sum([x[1] - x[0] + 1 for x in limits])


def get_distinct_accepts(
    workflows,
    current="in",
    limits={"x": [(1, 4000)], "m": [(1, 4000)], "a": [(1, 4000)], "s": [(1, 4000)]},
):
    if current == "R":
        return 0
    if current == "A":
        return prod([sum_limits(limits[x]) for x in limits])
    total = 0
    new_limits = limits.copy()
    for rule in workflows[current]:
        if not rule.op:
            total += get_distinct_accepts(workflows, rule.next, new_limits)
            continue
        current_split = split_limits(new_limits[rule.field], rule.op, rule.value)
        if rule.op == "<":
            next_split = split_limits(new_limits[rule.field], ">", rule.value - 1)
        else:
            next_split = split_limits(new_limits[rule.field], "<", rule.value + 1)
        new_limits[rule.field] = current_split
        total += get_distinct_accepts(workflows, rule.next, new_limits)
        new_limits[rule.field] = next_split
    return total


is_workflow = True
workflows = {}
parts = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        if len(line) == 0:
            is_workflow = False
            continue
        if is_workflow:
            d = line.split("{")
            workflows[d[0]] = list(map(Rule, d[1][:-1].split(",")))
        else:
            m = list(map(int, re.findall(r"\d+", line)))
            parts.append(dict(zip("xmas", m)))

print(f"Part 1: {get_rating_total(workflows, parts)}")
print(f"Part 2: {get_distinct_accepts(workflows)}")
