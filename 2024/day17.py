#!/usr/bin/python3

import re


class VM:

    def __init__(self, a, b, c, bytes):
        self.a = a
        self.b = b
        self.c = c
        self.bytes = bytes
        self.ip = 0
        self.output = []
        self._map = {
            0: lambda o: self.adv(o),
            1: lambda o: self.bxl(o),
            2: lambda o: self.bst(o),
            3: lambda o: self.jnz(o),
            4: lambda o: self.bxc(),
            5: lambda o: self.out(o),
            6: lambda o: self.bdv(o),
            7: lambda o: self.cdv(o),
        }

    def reset(self):
        self.a = self.b = self.c = self.ip = 0
        self.output.clear()

    def exec(self, halt_at_output=False):
        while self.ip < len(self.bytes):
            i, op = self.bytes[self.ip], self.bytes[self.ip + 1]
            self.ip += 2
            self._map[i](op)
            if halt_at_output and i == 5:
                return

    def adv(self, op):
        self.a >>= self.combo(op)

    def bxl(self, op):
        self.b ^= op

    def bst(self, op):
        self.b = self.combo(op) & 7

    def jnz(self, op):
        if self.a != 0:
            self.ip = op

    def bxc(self):
        self.b ^= self.c

    def out(self, op):
        v = self.combo(op) & 7
        self.output.append(v)

    def bdv(self, op):
        self.b = self.a >> self.combo(op)

    def cdv(self, op):
        self.c = self.a >> self.combo(op)

    def combo(self, op):
        if 0 <= op <= 3:
            return op
        if op == 4:
            return self.a
        if op == 5:
            return self.b
        if op == 6:
            return self.c
        raise (f"Invalid combo operation {op}")


# 2,4,1,5,7,5,0,3,4,1,1,6,5,5,3,0
# 2,4: b = a & 7
# 1,5: b ^= 5
# 7,5: c = a >> b
# 0,3: a >>= 3
# 4,1: b ^= c
# 1,6: b ^= 6
# 5,5: out b & 7
# 3,0: goto 0 if a != 0
#
# Working backward from out instruction
# out (((a & 7) ^ 5) ^ (a >> ((a & 7) ^ 5))))) ^ 6) & 7
#
# UPDATE: Populate vm with 'a' and run until first 'out'
def find_a(vm, data, i=0, a=0):
    if i == len(data):
        return a >> 3
    for a_digit in range(8):
        a_candidate = a + a_digit
        vm.reset()
        vm.a = a_candidate
        vm.exec(True)
        if vm.output[0] == data[i]:
            new_a = find_a(vm, data, i + 1, a_candidate << 3)
            if new_a:
                return new_a


with open("input.txt") as f:
    data = list(map(int, re.findall(r'(\d+)', f.read())))
vm = VM(data[0], data[1], data[2], data[3:])
vm.exec()
print(f"Part 1: {','.join(map(str, vm.output))}")

a = find_a(vm, list(reversed(data[3:])))
print(f"Part 2: {a}")
