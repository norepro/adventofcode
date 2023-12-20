#!/usr/bin/python3

import queue
import re
from collections import defaultdict
from math import lcm


class FlipFlopModule:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.is_on = False

    def handle_pulse(self, sender, is_high, queue):
        if not is_high:
            self.is_on = not self.is_on
            for target in self.targets:
                queue.enqueue_pulse(self.name, target, self.is_on)

    def reset(self):
        self.is_on = False


class ConjunctionModule:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.last_pulses = {}

    def handle_pulse(self, sender, is_high, queue):
        self.last_pulses[sender] = is_high
        send_pulse = not all(self.last_pulses.values())
        for target in self.targets:
            queue.enqueue_pulse(self.name, target, send_pulse)

    def register_input(self, sender):
        self.last_pulses[sender] = False

    def reset(self):
        for sender in self.last_pulses:
            self.last_pulses[sender] = False


class BroadcoasterModule:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

    def handle_pulse(self, sender, is_high, queue):
        for target in self.targets:
            queue.enqueue_pulse(self.name, target, is_high)

    def reset(self):
        pass


class PulseQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.reset()

    def enqueue_pulse(self, sender, target, is_high):
        self.queue.put((sender, target, is_high))

    def dequeue_pulse(self):
        pulse = self.queue.get()
        pulse_index = 1 if pulse[2] else 0
        self.counts[pulse[1]][pulse_index] += 1
        # pulse_type = "high" if pulse[2] else "low"
        # print(f"{pulse[0]} -{pulse_type}-> {pulse[1]}")
        return pulse

    def size(self):
        return self.queue.qsize()

    def reset(self):
        self.counts = defaultdict(lambda: [0, 0])


def create_module(string):
    m = re.match(r"(\S+) -> (.+)", string)
    sender, targets = m.groups()
    targets = list(map(str.strip, targets.split(",")))
    if sender.startswith("%"):
        return FlipFlopModule(sender[1:], targets)
    elif sender.startswith("&"):
        return ConjunctionModule(sender[1:], targets)
    else:
        return BroadcoasterModule(sender, targets)


def register_conjunction_inputs(modules):
    conjunction_modules = set(
        [modules[m].name for m in modules if isinstance(modules[m], ConjunctionModule)]
    )
    for module in modules:
        for cm in conjunction_modules.intersection(modules[module].targets):
            modules[cm].register_input(module)


def push_button(modules, pulse_queue):
    pulse_queue.enqueue_pulse("button", "broadcaster", False)
    while pulse_queue.size() > 0:
        pulse = pulse_queue.dequeue_pulse()
        if pulse[1] in modules:
            modules[pulse[1]].handle_pulse(pulse[0], pulse[2], pulse_queue)


# Prints a graphviz digraph of the modules
def print_digraph(modules):
    print("digraph G {")
    for module in modules:
        for target in module.targets:
            print(f"  {module.name} -> {target};")
    print("}")


modules = {}
with open("input.txt", "r") as f:
    for line in f:
        module = create_module(line)
        modules[module.name] = module
modules["button"] = BroadcoasterModule("button", ["broadcaster"])
register_conjunction_inputs(modules)

# Part 1
pq = PulseQueue()
for _ in range(1000):
    push_button(modules, pq)
low_count = sum([pq.counts[c][0] for c in pq.counts])
high_count = sum([pq.counts[c][1] for c in pq.counts])
print(f"Part 1: {low_count * high_count}")

pq.reset()
for module in modules:
    modules[module].reset()

# Part 2
#
# Graph visualization reveals that the broadcaster sends to N independent
# state machines whose results are each passed to a NAND (Conjunction)
# module. Those results are then passed through a final NAND to the rx module.
#
# For a single low pulse to rx, the previous NAND must receive high pulses
# from each of the final state machine NAND gates. For each of those NAND
# gates to emit a high pulse, they must themselves receive a low pulse.
#
# NB: I do not know a general answer to this :(
#
# First, identify the NAND gate before rx
rx_nand = [m for m in modules if "rx" in modules[m].targets][0]

# Identify the modules that feed into the rx NAND gate
ends = [m for m in modules if rx_nand in modules[m].targets]

# Count button presses for each of the sub machine NAND gates to receive a
# low pulse.
presses = 0
presses_required = []
while len(ends) > 0:
    push_button(modules, pq)
    presses += 1
    for i in range(len(ends) - 1, -1, -1):
        if pq.counts[ends[i]][0] == 1:
            presses_required.append(presses)
            del ends[i]
print(f"Part 2: {lcm(*presses_required)}")
