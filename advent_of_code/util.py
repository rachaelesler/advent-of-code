"""Utility functions for Advent of code 2024"""

TEMPLATE_OUTPUT = "Answer to day {0}, part {1}: "


def print_output_string(day: int, part: int):
    """Utility function for printing Advent of Code solutions."""
    print(TEMPLATE_OUTPUT.format(day, part), end="")


def file_contents_as_string(filepath: str) -> str:
    """Return the contents of a text file as a string.

    Args:
        filepath (str): Path to text file

    Returns:
        str: Contents of text file as a string
    """
    input_str = ""
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        for line in file:
            input_str += line
    return input_str
