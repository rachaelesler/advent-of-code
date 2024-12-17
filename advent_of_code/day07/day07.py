"""
Advent of Code 2024, day 7.
"""

from advent_of_code.day07.part1 import solve_part_one
from advent_of_code.day07.part2 import solve_part_two
from advent_of_code.util import print_output_string

INPUT_FILEPATH = "advent_of_code/day07/input.txt"
INPUT_FILEPATH_SMALL = "advent_of_code/day07/input_small.txt"


def main():
    print_output_string(7, 1)
    s = solve_part_one(INPUT_FILEPATH)
    print(s)

    print_output_string(7, 2)
    t = solve_part_two(INPUT_FILEPATH)
    print(t)
