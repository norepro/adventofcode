#!/usr/bin/env python3

import networkx as nx
import re
from collections import namedtuple

Op = namedtuple('Op', ['a', 'op', 'b', 'gate'])


class BinaryComputer:

    def __init__(self, gates, ops):
        self.gates = gates
        self.ops = ops
        self._op_lambdas = {
            'AND': lambda a, b: a & b,
            'OR': lambda a, b: a | b,
            'XOR': lambda a, b: a ^ b,
        }

    def exec(self):
        gates = self.gates.copy()
        ops = self.ops.copy()
        while len(ops):
            for op in ops:
                if op.a not in gates or op.b not in gates:
                    continue
                gates[op.gate] = self._op_lambdas[op.op](gates[op.a],
                                                         gates[op.b])
                break
            ops.remove(op)
        return gates


def make_graph(ops, label=False):
    g = nx.DiGraph()
    for op in ops:
        if label:
            g.add_node(op.gate, label=f'{op.gate} ({op.op})')
        g.add_edge(op.a, op.gate)
        g.add_edge(op.b, op.gate)
    return g


def get_num(gates, prefix):
    n = 0
    for gate in gates:
        if gate.startswith(prefix) and gates[gate] != 0:
            s = int(gate[1:])
            n += 1 << s
    return n


with open("input.txt") as f:
    data = f.read()
    gates = {m[0]: int(m[1]) for m in re.findall(r'(.+): (\d+)', data)}
    ops = [
        Op(m[0], m[1], m[2], m[3])
        for m in re.findall(r'(.+) (.+) (.+) -> (.+)', data)
    ]
bc = BinaryComputer(gates, ops)
print(f"Part 1: {get_num(bc.exec(), 'z')}")

g = make_graph(ops)
nx.nx_agraph.to_agraph(g).write('day24-unlabeled.dot')
g = make_graph(ops, True)
nx.nx_agraph.to_agraph(g).write('day24-labeled.dot')

print("Run the following commands to create the graphs:")
print("  dot -Tpng day24-labeled.dot -o day24-labeled.png")
print("  dot -Tpng day24-unlabeled.dot -o day24-unlabeled.png")
print()
