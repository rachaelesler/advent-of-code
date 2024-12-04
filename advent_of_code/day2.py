"""
Advent of code 2024 day 2.
"""

from advent_of_code import util
from typing import List
from copy import deepcopy

INPUT_DAY2_PATH = "advent_of_code/input_day2.txt"


def main():
    util.print_output_string(2, 1)
    print(count_safe_reports(INPUT_DAY2_PATH))
    util.print_output_string(2, 2)
    print(count_safe_reports(INPUT_DAY2_PATH, True))


def count_safe_reports(filepath: str, allow_bad_level=False) -> int:
    """Count the number of safe reports for a given file.

    Each row in the given file should correspond to a 'report', with each item
    in the row corresponding to a 'level'.
    """
    safe_count = 0
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        for line in file:
            # Iterate through each report, formatting as we go
            report = line.strip("\n").split()
            if is_report_safe(report, allow_bad_level):
                safe_count += 1
    return safe_count


def is_report_safe(report: List[str], allow_bad_level=False) -> bool:
    """Return True if a report is safe, False otherwise.

    A report is safe if both of the following are true:
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.

    If `allow_bad_level` is True, then if removing a single level from an
    unsafe report would make it safe, the report instead counts as safe.
    """
    length = len(report)

    for i in range(1, length - 1):
        prev_lvl = int(report[i - 1])
        current_lvl = int(report[i])
        next_lvl = int(report[i + 1])

        if not (prev_lvl < current_lvl < next_lvl):
            if not (prev_lvl > current_lvl > next_lvl):
                # Not increasing or decreasing, not safe
                if not allow_bad_level:
                    return False
                # Check if report is safe with any of these items removed
                return (
                    is_report_safe_without_item(report, i - 1)
                    or is_report_safe_without_item(report, i)
                    or is_report_safe_without_item(report, i + 1)
                )

        # Compare previous and current level difference
        if not difference_is_between_one_and_three(prev_lvl, current_lvl):
            if not allow_bad_level:
                return False
            return is_report_safe_without_item(report, i - 1) or is_report_safe_without_item(report, i)

    # Finally compare last two levels not compared in loop
    if difference_is_between_one_and_three(int(report[-1]), int(report[-2])):
        return True
    elif allow_bad_level:
        return is_report_safe_without_item(report, -1) or is_report_safe_without_item(report, -2)
    return False


def is_report_safe_without_item(report: List[str], index: int) -> bool:
    """Returns True if the given report would be safe if the item at the given
    index was removed, False otherwise.
    """
    report_without_item = deepcopy(report)
    report_without_item.pop(index)
    return is_report_safe(report_without_item)


def difference_is_between_one_and_three(first: int, second: int):
    """Return True if first and second number differ by at least one and at
    most three, False otherwise.
    """
    return 1 <= abs(first - second) <= 3
