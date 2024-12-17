import itertools
from typing import Iterator, List

from advent_of_code.day07.common import load_input


def solve_part_two(filepath: str) -> int:
    result = 0
    problem_arr = load_input(filepath)
    for test_val, equation_vals in problem_arr:
        if can_equation_be_made_true(test_val, equation_vals):
            result += test_val
    return result


def can_equation_be_made_true(test_val: int, equation_vals: List[int]) -> bool:
    n = len(equation_vals)
    # Try all operator combinations for the current equation until we find one that works
    combinations = get_all_operator_combinations_including_concat(n)
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
            if operation == 2:
                equation_result = int(f"{equation_result}{val}")

        if equation_result == test_val:
            return True
    return False


def get_all_operator_combinations_including_concat(count: int) -> Iterator:
    """Get an Iterator with all possible combinations of operators.

    Args:
        count (int): Number of values in the input eqiation.

    Returns:
        Iterator: Contains lists of integers representing all possible unique combinations and
        permuations of operators for the given `count`.
    """
    return itertools.product([0, 1, 2], repeat=count - 1)
