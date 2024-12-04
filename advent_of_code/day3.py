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


def main() -> None:
    # Read file input into a string
    input_str = ""
    with open(
        INPUT_DAY3_PATH,
        encoding="utf-8",
    ) as file:
        for line in file:
            input_str += line

    # print(re.escape(input_str))
    # # Use regex to find all matches in the input string
    # input_str = r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    matches = re.findall(MUL_BRACKETS_REGEX, (input_str))
    output = 0
    for match in matches:
        output += mul_string_to_number(match)
    util.print_output_string(3, 1)
    print(output)


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
