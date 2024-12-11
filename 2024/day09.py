#!/usr/bin/python3


class Block:

    def __init__(self, id, offset, length):
        self.id = id
        self.offset = offset
        self.length = length
        self.prev = None
        self.next = None

    def append(self, block):
        block.prev = self
        block.next = self.next
        if block.next:
            block.next.prev = block
        self.next = block

    def __repr__(self) -> str:
        return f"Block({self.id},{self.offset},{self.length})"


class Filesystem:

    def __init__(self, input):
        self.first_block = None
        self.last_block = None
        cur_id, offset = 0, 0
        is_free = False
        for c in input:
            c = int(c)
            id = -1 if is_free else cur_id
            block = Block(id, offset, c)
            if not self.first_block:
                self.first_block = block
            else:
                block.prev = self.last_block
                self.last_block.next = block
            self.last_block = block
            is_free = not is_free
            if id != -1:
                cur_id += 1
            offset += c
        self.__prune_trailing_free_blocks()

    def get_blocks(self):
        block = self.first_block
        while block:
            yield block
            block = block.next

    def compact_blocks(self):
        for block in self.get_blocks():
            if block.id != -1:
                block = block.next
                continue
            n = min(block.length, self.last_block.length)
            block.id = self.last_block.id
            if n == block.length:
                self.last_block.length -= n
                self.__prune_trailing_free_blocks()
            else:
                self.last_block.id = -1
                free_block = Block(-1, block.offset + n, block.length - n)
                block.append(free_block)
                block.length = n
                self.__prune_trailing_free_blocks()

    def compact_files(self):
        file = self.last_block
        while file:
            if file.id == -1:
                file = file.prev
                continue
            for block in self.get_blocks():
                if block.id == -1 and block.offset < file.offset and block.length >= file.length:
                    block.id = file.id
                    file.id = -1
                    n = block.length - file.length
                    block.length = file.length
                    if n > 0:
                        free_block = Block(-1, block.offset + file.length, n)
                        block.append(free_block)
                    break
            file = file.prev

    def get_checksum(self):
        checksum = 0
        for block in self.get_blocks():
            if block.id != -1:
                for i in range(block.length):
                    checksum += block.id * (block.offset + i)
        return checksum

    def print(self):
        for b in self.get_blocks():
            id = "." if b.id == -1 else str(b.id)
            print(id * b.length, end='')
        print()

    def __prune_trailing_free_blocks(self):
        block = self.last_block
        while block and (block.length == 0 or block.id == -1):
            block = block.prev
            if block:
                block.next = None
        self.last_block = block


with open("input.txt") as f:
    d = f.read().rstrip()
fs = Filesystem(d)
fs.compact_blocks()

print(f"Part 1: {fs.get_checksum()}")

# TODO: Make faster by caching earliest free block per size
fs = Filesystem(d)
fs.compact_files()
print(f"Part 2: {fs.get_checksum()}")
