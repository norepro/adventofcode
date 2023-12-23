#!/usr/bin/python3

import uuid
import queue
from tqdm import tqdm


class Brick:
    def __init__(self, p1, p2, id=None):
        self.id = id or uuid.uuid4()
        self.p1 = p1
        self.p2 = p2
        self.x_range = range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1)
        self.y_range = range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1)
        self.z_range = range(min(p1[2], p2[2]), max(p1[2], p2[2]) + 1)
        self.above = set()
        self.below = set()

    def __repr__(self) -> str:
        return f"Brick({self.p1},{self.p2},'{self.id}')"

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id

    def __hash__(self) -> int:
        return self.id.__hash__()

    def does_intersect(self, brick):
        x0 = max(self.x_range.start, brick.x_range.start)
        x1 = min(self.x_range.stop, brick.x_range.stop)

        if x0 >= x1:
            return False

        x0 = max(self.y_range.start, brick.y_range.start)
        x1 = min(self.y_range.stop, brick.y_range.stop)

        if x0 >= x1:
            return False

        x0 = max(self.z_range.start, brick.z_range.start)
        x1 = min(self.z_range.stop, brick.z_range.stop)
        return x0 < x1

    def translate(self, x, y, z):
        return Brick(
            (self.p1[0] + x, self.p1[1] + y, self.p1[2] + z),
            (self.p2[0] + x, self.p2[1] + y, self.p2[2] + z),
            self.id,
        )


# TODO: This is very slow, about one minute for actual input. Correct approach
# is creating a graph without actually collapsing the bricks.
def settle(bricks):
    adjustments = float("inf")
    while adjustments > 0:
        adjustments = 0
        for i in range(len(bricks) - 1, -1, -1):
            b = bricks[i]
            if b.z_range.start < 2:
                continue
            candidate = b.translate(0, 0, -1)
            for brick in bricks:
                if brick.z_range.start >= b.z_range.start or brick.id == b.id:
                    continue
                if candidate.does_intersect(brick):
                    break
            else:
                # Nothing preventing candidate from falling
                bricks[i] = candidate
                adjustments += 1


def create_brick_links(bricks):
    for source in tqdm(bricks, desc="Creating Brick Links"):
        above = source.translate(0, 0, 1)
        for target in bricks:
            if source.id == target.id:
                continue
            if above.does_intersect(target):
                source.above.add(target)
                target.below.add(source)


def save_bricks_to_file(bricks, file):
    with open(file, "w") as w:
        for b in bricks:
            w.write(f"{b.p1[0]},{b.p1[1]},{b.p1[2]}~{b.p2[0]},{b.p2[1]},{b.p2[2]}\n")


def get_triggered_bricks(brick):
    to_fall = set([brick])
    original_brick = brick
    q = queue.Queue()
    for b in brick.above:
        q.put(b)
    while not q.empty():
        brick = q.get()
        if len(brick.below.difference(to_fall)) > 0:
            # Supported by a non-falling brick, chain stops
            continue
        to_fall.add(brick)
        for b in brick.above:
            q.put(b)
    to_fall.remove(original_brick)
    return to_fall


def part1(bricks):
    remove_count = 0
    for brick in bricks:
        if len(brick.above) == 0:
            remove_count += 1
        else:
            # Check if we are the only brick supporting these
            for id in brick.above:
                if len(id.below) == 1:
                    break
            else:
                remove_count += 1
    print(f"Part 1: {remove_count}")


def part2(bricks):
    total_will_fall = 0
    for brick in bricks:
        total_will_fall += len(get_triggered_bricks(brick))
    print(f"Part 2: {total_will_fall}")


bricks = []
with open("input.txt", "r") as f:
    for line in f:
        brick = list(
            map(lambda x: tuple(map(int, x.split(","))), line.rstrip().split("~"))
        )
        bricks.append(Brick(brick[0], brick[1]))
settle(bricks)
# save_bricks_to_file(bricks, "input-optimized.txt")
create_brick_links(bricks)
part1(bricks)
part2(bricks)
