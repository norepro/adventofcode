#!/usr/bin/python3


def get_maximum_joltage(digits: list[int], n_digits: int):
    start = 0
    maximum_joltage = 0
    while n_digits > 0:
        i, n = get_max_digit(digits, start, len(digits) - n_digits + 1)
        maximum_joltage += n * 10**(n_digits - 1)
        start = i + 1
        n_digits -= 1
    return maximum_joltage


def get_max_digit(digits: list[int], start: int, stop: int):
    max_digit = 0
    max_index = 0
    for i in range(start, stop):
        n = digits[i]
        if n > max_digit:
            max_digit = n
            max_index = i
            if max_digit == 9:
                break
    return (max_index, max_digit)


def main():
    sum_max_2 = 0
    sum_max_12 = 0
    with open('input.txt') as f:
        for line in f:
            digits = list(map(int, line.rstrip()))
            sum_max_2 += get_maximum_joltage(digits, 2)
            sum_max_12 += get_maximum_joltage(digits, 12)
    return sum_max_2, sum_max_12


if __name__ == '__main__':
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
