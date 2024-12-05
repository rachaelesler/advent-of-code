"""
Advent of code 2024 day 3.

Part one:
Interpret multiplication instructions from a jumbled file of instructions and
print the sum of all the multiplications.
"""

import re
from advent_of_code import util

INPUT_DAY3_PATH = "advent_of_code/input_day3.txt"
MUL_BRACKETS_REGEX = r"mul\(([0-9]+,[0-9]+)\)"
DONT_INSTRUCTION = r"don't()"
DO_INSTRUCTION = r"do()"


def main() -> None:
    """Calculate and print the solution to Advent of Code 2024, day 3."""
    input_str = read_input_str(INPUT_DAY3_PATH)
    # Use regex to find all matches in the input string
    util.print_output_string(3, 1)
    print(find_and_multiply_all_mul_strings(input_str))
    util.print_output_string(3, 2)
    part_two = solve_part_two(input_str)
    print(part_two)


def find_and_multiply_all_mul_strings(input_str: str) -> int:
    matches = re.findall(MUL_BRACKETS_REGEX, (input_str))
    output = 0
    for match in matches:
        output += mul_string_to_number(match)
    return output


def solve_part_two(input_str: str) -> int:
    # Take input string and split wherever we find a `don't()` instruction
    split_input = input_str.split(DONT_INSTRUCTION)
    output = 0
    # For each item in list, consider everything after a `do()`
    for item in split_input:
        instructions_to_keep = item.split(DO_INSTRUCTION)[1:]
        for instruction in instructions_to_keep:
            output += find_and_multiply_all_mul_strings(instruction)
    return output


def read_input_str(filepath: str) -> str:
    """Return the contents of file at `filepath` into a string."""
    input_str = ""
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        for line in file:
            input_str += line
    return input_str


def mul_string_to_number(mul_str: str) -> int:
    """Interprets a string in the format "mul(x,y)" (where x and y are
    integers) and outputs the product of x and y.

    Args:
        mul_str (str): string in the format "mul(x,y)"

    Returns:
        int: product of two numbers encoded in input string
    """
    # Strip "mul" from the start, and brackets
    mul_str = mul_str.strip("mul").strip("(").strip(")")
    numbers = mul_str.split(",")
    return int(numbers[0]) * int(numbers[1])
