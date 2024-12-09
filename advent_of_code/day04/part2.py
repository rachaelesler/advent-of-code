"""
Functions for Advent of Code day 4, part 2.
"""

from dataclasses import dataclass
from typing import List
from advent_of_code.day04.classes import Direction, SearchPath
from advent_of_code.day04.common import is_target_in_search_path

TARGET_WORD = "MAS"
SEARCH_DIRECTIONS = [
    Direction.BOTTOM_LEFT,
    Direction.BOTTOM_RIGHT,
    Direction.TOP_LEFT,
    Direction.TOP_RIGHT,
]
DEFAULT_CHARACTER = "."


@dataclass
class BoolAndSearchPath:
    bool_value: bool
    search_path: SearchPath


def count_x_shaped_mas_in_wordsearch(wordsearch_arr: List) -> int:
    """Count how many times the X-shaped "MAS" pattern appears in a word
    search.

    Args:
        wordsearch_arr (List): List where each item is a list representing
        a row in the wordsearch.
    """
    times_target_appears = 0
    n_rows = len(wordsearch_arr)
    for curr_row in range(n_rows):
        n_cols = len(wordsearch_arr[curr_row])
        for curr_col in range(n_cols):
            # Iterate through each position in the wordsearch
            result = is_position_part_of_x_shaped_mas(
                wordsearch_arr, curr_row, curr_col
            )
            if result.bool_value:
                times_target_appears += 1
                # Remove the "A" that forms part of the pattern, so we don't
                # count this pattern twice
                wordsearch_arr[curr_row + result.search_path.row_increment][
                    curr_col + result.search_path.col_increment
                ] = DEFAULT_CHARACTER

    return times_target_appears


def is_position_part_of_x_shaped_mas(
    wordsearch_arr: List, curr_row: int, curr_col: int
) -> BoolAndSearchPath:
    """Return True if the current position in the word search forms an X-shaped
    "MAS" or "SAM" pattern, False otherwise.

    Also return the direction that the centre of the "X" was found in.
    """
    target_word = TARGET_WORD
    if wordsearch_arr[curr_row][curr_col] == TARGET_WORD[-1]:
        target_word = reversed_string(TARGET_WORD)
    elif wordsearch_arr[curr_row][curr_col] != TARGET_WORD[0]:
        # Position does not correctpond to "M" or "S"
        return BoolAndSearchPath(False, None)

    # If we reach an "M" or "S", search in all diagonal directions to see if it
    # makes "MAS" or "SAM"
    for direction in SEARCH_DIRECTIONS:
        search_path = SearchPath(direction)
        if is_target_in_search_path(
            search_path,
            wordsearch_arr,
            curr_row,
            curr_col,
            target_word,
        ):
            # If "MAS" or "SAM" is found, check if it part of the full X
            # pattern
            if find_second_part_of_x_shaped_mas(
                wordsearch_arr, curr_row, curr_col, direction
            ):
                return BoolAndSearchPath(True, search_path)
    return BoolAndSearchPath(False, None)


def find_second_part_of_x_shaped_mas(
    wordsearch_arr: List, curr_row: int, curr_col: int, direction: Direction
) -> bool:
    """Assuming "MAS" was found in `direction` with the "M" at `curr_row`,
    `curr_col`, return True if it part of an X-shaped "MAS" pattern, False
    otherwise.

    Args:
        wordsearch_arr (List):  List where each item is a list representing
        a row in the wordsearch.
        curr_row (int): Row position of M that is part of a "MAS"
        curr_col (int): Column position of M that is part of a "MAS"
        direction (Direction): Direction that the "MAS" was found in, starting
        from the "M"
    """
    match direction:
        case Direction.BOTTOM_LEFT:
            # Pattern found was:
            # ..M
            # .A.
            # S..
            return is_target_or_reverse_in_search_path(
                SearchPath(Direction.BOTTOM_RIGHT),
                wordsearch_arr,
                curr_row,
                curr_col - 2,
                TARGET_WORD,
            )
        case Direction.BOTTOM_RIGHT:
            # Pattern found was:
            # M..
            # .A.
            # ..S
            return is_target_or_reverse_in_search_path(
                SearchPath(Direction.BOTTOM_LEFT),
                wordsearch_arr,
                curr_row,
                curr_col + 2,
                TARGET_WORD,
            )
        case Direction.TOP_LEFT:
            # Pattern found was:
            # S..
            # .A.
            # ..M
            return is_target_or_reverse_in_search_path(
                SearchPath(Direction.TOP_RIGHT),
                wordsearch_arr,
                curr_row,
                curr_col - 2,
                TARGET_WORD,
            )
        case Direction.TOP_RIGHT:
            # Pattern found was:
            # ..S
            # .A.
            # M..
            return is_target_or_reverse_in_search_path(
                SearchPath(Direction.TOP_LEFT),
                wordsearch_arr,
                curr_row,
                curr_col + 2,
                TARGET_WORD,
            )
        case _:
            raise ValueError("Invalid direction")


def is_target_or_reverse_in_search_path(
    search_path: SearchPath,
    wordsearch_arr,
    curr_row: int,
    curr_col: int,
    target_word: str,
):
    """Same as `is_target_in_search_path`, but also returns True if the reverse
    of the target word is in the specified search path.
    """
    if wordsearch_arr[curr_row][curr_col] == target_word[0]:
        # First letter is "M", search for "MAS"
        return is_target_in_search_path(
            search_path, wordsearch_arr, curr_row, curr_col, target_word
        )
    if wordsearch_arr[curr_row][curr_col] == target_word[-1]:
        # First letter is "S", search for "SAM"
        return is_target_in_search_path(
            search_path,
            wordsearch_arr,
            curr_row,
            curr_col,
            reversed_string(target_word),
        )
    return False


def reversed_string(a_string: str) -> str:
    """Return the reverse of the input string."""
    return a_string[::-1]
