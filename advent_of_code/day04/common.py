from advent_of_code.day04.classes import Direction, SearchPath


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
) -> bool:
    """Return True if the target word is in the specified search path, False
    otherwise.

    The search must start from the first letter of the target word.
    """
    if wordsearch_arr[curr_row][curr_col] == target_word[0]:
        return _is_target_in_search_path(
            search_path, wordsearch_arr, curr_row, curr_col, target_word
        )
    raise ValueError("Must search from first letter of target word")


def _is_target_in_search_path(
    search_path: SearchPath,
    wordsearch_arr,
    curr_row: int,
    curr_col: int,
    target_word: str,
):
    """Recursive function to search through wordsearch for the target word.

    Returns True once the search reaches the last letter of the target word,
    indicating the search is complete. The function is called again if the next
    letter is correct.

    This function assumes that all letters in the target word are unique!

    Returns False if the search would go outside the limits of the wordsearch,
    or if the search path does not contain the correct word.
    """
    curr_char = wordsearch_arr[curr_row][curr_col]
    if curr_char == target_word[-1]:
        # Return when we reach the last letter of the word
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
    if next_char == get_correct_next_letter(curr_char, target_word):
        # If next character is correct, keep searching
        return _is_target_in_search_path(
            search_path, wordsearch_arr, next_row, next_col, target_word
        )
    # Next character is not correct; the word does not appear to the right
    return False
