"""Advent of Code 2024, day 4."""

from typing import List
from advent_of_code import util
from advent_of_code.day04.classes import Direction, SearchPath

INPUT_FILEPATH = "advent_of_code/day04/input_day04.txt"

next_char_lookup = {"X": "M", "M": "A", "A": "S", "S": None}
FIRST_CHAR = "X"
FINAL_CHAR = "S"


def main() -> None:
    wordsearch_arr = wordsearch_file_to_array(INPUT_FILEPATH)

    util.print_output_string(4, 1)
    print(count_target_word_in_wordsearch(wordsearch_arr))


def count_target_word_in_wordsearch(wordsearch_arr) -> int:
    times_xmas_appears = 0
    n_rows = len(wordsearch_arr)
    for curr_row in range(n_rows):
        n_cols = len(wordsearch_arr[curr_row])
        for curr_col in range(n_cols):
            # Only search from the letter "X"
            if wordsearch_arr[curr_row][curr_col] == FIRST_CHAR:
                # Search in every direction
                for direction in Direction:
                    search_path = SearchPath(direction)
                    if is_target_in_search_path(
                        search_path, wordsearch_arr, curr_row, curr_col
                    ):
                        times_xmas_appears += 1
    return times_xmas_appears


def wordsearch_file_to_array(filepath: str) -> List[str]:
    wordsearch = []
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        # Interpret each line as an array
        for line in file:
            line = line.strip("\n")
            wordsearch.append(list(line))
    return wordsearch


def is_target_in_search_path(
    search_path: SearchPath,
    wordsearch_arr,
    curr_row: int,
    curr_col: int,
) -> bool:
    """Return True if the word "XMAS" is in the specified search path, False
    otherwise.

    The search must start from the letter "X".
    """
    if wordsearch_arr[curr_row][curr_col] == FIRST_CHAR:
        return _is_target_in_search_path(
            search_path, wordsearch_arr, curr_row, curr_col
        )
    raise ValueError("Tried to start searching from a letter other than X")


def _is_target_in_search_path(
    search_path: SearchPath,
    wordsearch_arr,
    curr_row: int,
    curr_col: int,
):
    """Recursive function to search through wordsearch for the word "XMAS".

    Returns True once the search reaches the letter "S", indicating the search
    is complete. The function is called again if the next letter is correct.

    Returns False if the search would go outside the limits of the wordsearch,
    or if the search path does not contain the correct word.
    """
    curr_char = wordsearch_arr[curr_row][curr_col]
    if curr_char == FINAL_CHAR:
        # Return when we reach the letter "S"
        return True
    next_row = curr_row + search_path.row_increment
    next_col = curr_col + search_path.col_increment

    # Check if next row or col would be off wordsearch
    if (
        next_row >= len(wordsearch_arr)
        or next_col >= len(wordsearch_arr[curr_row])
        or next_row < 0
        or next_col < 0
    ):
        return False

    next_char = wordsearch_arr[next_row][next_col]
    if next_char == next_char_lookup[curr_char]:
        # If next character is correct, keep searching
        return _is_target_in_search_path(
            search_path, wordsearch_arr, next_row, next_col
        )
    # Next character is not correct; the word does not appear to the right
    return False
