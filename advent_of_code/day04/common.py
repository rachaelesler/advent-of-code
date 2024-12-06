"""
Common functionality for Advent of Code 2024, day 4, part 1 and 2.
"""

from advent_of_code.day04.classes import SearchPath


def wordsearch_file_to_array(filepath: str):
    """Convert the wordsearch file at `filepath` to an array and return.

    Each item in the array is an array representing a row in the wordsearch.
    """
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


def get_correct_next_letter(current_letter: str, target_word: str):
    """Given the current character in a word, return the next letter; return
    None if the current character is the last character.

    Assumes all letters in target_word are unique!
    """
    if current_letter == target_word[-1]:
        return None
    return target_word[target_word.index(current_letter) + 1]


def is_target_in_search_path(
    search_path: SearchPath,
    wordsearch_arr,
    curr_row: int,
    curr_col: int,
    target_word: str,
):
    """Return True if the target word is in the specified search path, False
    otherwise.

    Recursive function to search through wordsearch for the target word.

    Returns True once the search reaches the last letter of the target word,
    indicating the search is complete. The function is called again if the next
    letter is correct.

    This function assumes that all letters in the target word are unique!

    Returns False if the search would go outside the limits of the wordsearch,
    or if the search path does not contain the correct word.
    """
    curr_char = wordsearch_arr[curr_row][curr_col]
    if curr_char == target_word[-1]:
        # Return True when we reach the last letter of the word
        return True

    # Work out the next letter based on the direction we are searching in
    next_row = curr_row + search_path.row_increment
    next_col = curr_col + search_path.col_increment

    # Check if position would be off limits of wordsearch. If so, return False.
    if (
        next_row >= len(wordsearch_arr)
        or next_col >= len(wordsearch_arr[curr_row])
        or next_row < 0
        or next_col < 0
    ):
        return False

    next_char = wordsearch_arr[next_row][next_col]
    if next_char == get_correct_next_letter(curr_char, target_word):
        # If next character is correct, keep searching
        return is_target_in_search_path(
            search_path, wordsearch_arr, next_row, next_col, target_word
        )
    # Next character is not correct
    return False
