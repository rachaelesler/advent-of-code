"""
Advent of Code 2024, day 7.
"""

import itertools
from typing import Iterator, List

from advent_of_code.util import print_output_string

INPUT_FILEPATH = "advent_of_code/day07/input.txt"
INPUT_FILEPATH_SMALL = "advent_of_code/day07/input_small.txt"


def main():
    print_output_string(7, 1)
    s = solve_part_one(INPUT_FILEPATH)
    print(s)


def solve_part_one(filepath: str) -> int:
    result = 0
    problem_arr = load_input(filepath)
    for test_val, equation_vals in problem_arr:
        if can_equation_be_made_true(test_val, equation_vals):
            result += test_val
    return result


def load_input(filepath: str) -> List:
    output = []
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        for line in file:
            line_arr = line.split(":")
            test_val = int(line_arr[0])
            equation_vals = [int(x) for x in line_arr[1].strip().strip("\n").split(" ")]
            output.append([test_val, equation_vals])
    return output


def can_equation_be_made_true(test_val: int, equation_vals: List[int]) -> bool:
    n = len(equation_vals)
    # Try all operator combinations for the current equation until we find one that works
    combinations = get_all_operator_combinations(n)
    for combination in combinations:
        equation_result = equation_vals[0]
        # Iterate through each number in the equation, and each operation
        for idx in range(0, n - 1):
            # Apply each operation in the combination from left to right
            operation = combination[idx]
            val = equation_vals[idx + 1]
            if operation == 0:
                equation_result += val
            if operation == 1:
                equation_result *= val

        if equation_result == test_val:
            return True
    return False


def get_all_operator_combinations(count: int) -> Iterator:
    """Get an Iterator with all possible combinations of operators.

    Args:
        count (int): Number of values in the input eqiation.

    Returns:
        Iterator: Contains lists of integers representing all possible unique combinations and
        permuations of operators for the given `count`.
    """
    return itertools.product([0, 1], repeat=count - 1)
