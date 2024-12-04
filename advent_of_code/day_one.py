"""
Advent of code 2024 day 1.

Part one:
Calculate the distance between the Historian's two lists.

Part two:
Calculate the similarity score between the Historian's two lists (add up each
number in the left list after multiplying it by the number of times it appears
in the right list).
"""

from advent_of_code import util, constants
from advent_of_code.historian_list import HistorianList


def main():
    my_historian_list = HistorianList(constants.HISTORIAN_LIST_PATH)
    # Part one
    util.print_output_string(1, 1)
    print(my_historian_list.distance)
    # Part two
    util.print_output_string(1, 2)
    print(my_historian_list.similarity)
