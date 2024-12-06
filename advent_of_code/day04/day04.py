"""
Advent of Code 2024, day four.
"""

from advent_of_code import util
from advent_of_code.day04.common import wordsearch_file_to_array
from advent_of_code.day04.part1 import count_xmas_in_wordsearch
from advent_of_code.day04.part2 import count_x_shaped_mas_in_wordsearch


INPUT_FILEPATH = "advent_of_code/day04/input_day04.txt"


def main() -> None:
    """Calculate and print the solution to Advent of Code 2024, day 4."""
    wordsearch_arr = wordsearch_file_to_array(INPUT_FILEPATH)

    util.print_output_string(4, 1)
    print(count_xmas_in_wordsearch(wordsearch_arr))

    util.print_output_string(4, 2)
    print(count_x_shaped_mas_in_wordsearch(wordsearch_arr))
