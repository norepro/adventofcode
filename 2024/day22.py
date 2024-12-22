#!/usr/bin/env python3

from tqdm import tqdm


def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    return prune(mix(secret, secret * 2048))


def mix(secret, n):
    return n ^ secret


def prune(secret):
    return secret % 16777216


with open("input.txt") as f:
    secrets = [int(x) for x in f]

seq_banana_map = {}
p1 = 0
with tqdm(total=len(secrets)) as t:
    for si, secret in enumerate(secrets):
        t.update(1)
        digits = [secret % 10]
        for i in range(2000):
            secret = next_secret(secret)
            digits.append(secret % 10)
            if i > 3:
                s = (digits[i - 3] - digits[i - 4],
                     digits[i - 2] - digits[i - 3],
                     digits[i - 1] - digits[i - 2], digits[i] - digits[i - 1])
                maxes = seq_banana_map.get(s)
                if not maxes:
                    maxes = [0] * len(secrets)
                    seq_banana_map[s] = maxes
                if maxes[si] == 0:
                    maxes[si] = digits[i]
        p1 += secret
best_seq, best_total = None, 0
for seq in seq_banana_map:
    s = sum(seq_banana_map[seq])
    if s > best_total:
        best_seq = seq
        best_total = s
print(f"Part 1: {p1}")
print(f"Part 2: {best_total}, {best_seq}")
