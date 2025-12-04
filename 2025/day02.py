#!/usr/bin/python3

from functools import cache


@cache
def is_repeated_seq(s: str):
    for i in range(1, len(s) // 2 + 1):
        seq = s[:i]
        for j in range(i, len(s), i):
            if seq != s[j:j + i]:
                break
        else:
            return True
    return False


def main():
    two_invalid_sum = 0
    all_invalid_sum = 0

    with open("input.txt") as f:
        data = [x.split("-") for x in f.readline().split(",")]

    for range_ in data:
        range_lower, range_upper = int(range_[0]), int(range_[1])
        for num_digits in range(len(range_[0]), len(range_[1]) + 1):
            lower_str = str(max(range_lower, 10**(num_digits - 1)))
            upper_str = str(min(range_upper, (10**num_digits) - 1))
            for repeat_size in range(1, (num_digits // 2) + 1):
                if num_digits % repeat_size != 0:
                    continue
                lower_repeat = int(lower_str[:repeat_size])
                upper_repeat = int(upper_str[:repeat_size])
                num_repeats = num_digits // repeat_size
                for i in range(lower_repeat, upper_repeat + 1):
                    i_str = str(i)
                    n = int(i_str * num_repeats)
                    if range_lower <= n <= range_upper:
                        if not is_repeated_seq(i_str):
                            all_invalid_sum += n
                        if num_repeats == 2:
                            two_invalid_sum += n
    return two_invalid_sum, all_invalid_sum


if __name__ == "__main__":
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
