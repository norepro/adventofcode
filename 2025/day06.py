#!/usr/bin/python3


class Solution:
    def __init__(self, path: str):
        with open(path) as f:
            lines = f.readlines()
            self.ops = []
            self.numbers = [[] for _ in range(len(lines) - 1)]

            last_index = 0
            for i in range(1, len(lines[-1])):
                if lines[-1][i] != " " and lines[-1][i] != "\n":
                    self.ops.append(lines[-1][last_index])
                    for j in range(len(lines) - 1):
                        self.numbers[j].append(lines[j][last_index : i - 1])
                    last_index = i
            self.ops.append(lines[-1][last_index])
            for j in range(len(lines) - 1):
                self.numbers[j].append(lines[j][last_index:].rstrip("\n"))

    def run(self):
        first_sum = self.first_method()
        second_sum = self.second_method()
        return first_sum, second_sum

    def first_method(self):
        result = 0
        for i in range(len(self.ops)):
            n = int(self.numbers[0][i])
            for ni in range(1, len(self.numbers)):
                number = int(self.numbers[ni][i])
                if self.ops[i] == "+":
                    n += number
                else:
                    n *= number
            result += n
        return result

    def second_method(self):
        result = 0
        for i in range(len(self.ops)):
            op = self.ops[i]
            n = 0 if op == "+" else 1
            num_digits = len(self.numbers[0][i])
            for j in range(num_digits):
                number = ""
                for ni in range(len(self.numbers)):
                    c = self.numbers[ni][i][j]
                    if c != " ":
                        number += c
                if op == "+":
                    n += int(number)
                else:
                    n *= int(number)
            result += n
        return result


def main():
    solution = Solution("input.txt")
    return solution.run()


if __name__ == "__main__":
    p1, p2 = main()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
