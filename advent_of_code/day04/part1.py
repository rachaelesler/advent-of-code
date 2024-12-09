"""Functions for Advent of Code 2024, day 4, part 1."""

from typing import List
from advent_of_code.day04.classes import Direction, SearchPath
from advent_of_code.day04.common import is_target_in_search_path

TARGET_WORD = "XMAS"


def count_xmas_in_wordsearch(wordsearch_arr: List) -> int:
    """Return how many times the word "XMAS" appears in a word search.

    Args:
        wordsearch_arr (List): List where each item is a list representing
        a row in the wordsearch.
    """
    times_target_appears = 0
    n_rows = len(wordsearch_arr)
    for curr_row in range(n_rows):
        n_cols = len(wordsearch_arr[curr_row])
        for curr_col in range(n_cols):
            # Only search from the first letter of target_word
            if wordsearch_arr[curr_row][curr_col] == TARGET_WORD[0]:
                # Search in every direction
                for direction in Direction:
                    search_path = SearchPath(direction)
                    if is_target_in_search_path(
                        search_path,
                        wordsearch_arr,
                        curr_row,
                        curr_col,
                        TARGET_WORD,
                    ):
                        times_target_appears += 1
    return times_target_appears
