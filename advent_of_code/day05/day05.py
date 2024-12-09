"""
Solution for Advent of Code 2024, day 5.
"""

from typing import List
from dataclasses import dataclass
from advent_of_code.util import print_output_string, file_contents_as_string


INPUT_FILEPATH = "advent_of_code/day05/input_day05.txt"
INPUT_FILEPATH_SMALL = "advent_of_code/day05/input_day05_small.txt"


def main() -> None:
    """Compute and print the solution to Advent of Code 2024, day 5."""
    problem_input = ProblemInput(file_contents_as_string(INPUT_FILEPATH))

    print_output_string(5, 1)
    print(problem_input.solve_part_one())

    print_output_string(5, 2)
    print(problem_input.solve_part_two())


@dataclass
class OrderingRule:
    """A page ordering rule. Indicates that the `first_page` must be printed
    at some point before the `second_page` in all updates.
    """

    first_page: int
    second_page: int

    def __str__(self):
        return f"{self.first_page}|{self.second_page}"

    def contains(self, target: int) -> bool:
        """Return True if this rule involves the specified target number,
        False otherwise.
        """
        return (self.first_page == target) or (self.second_page == target)


class PageList:
    """Pages to print in a given update."""

    def __init__(
        self, page_list: List[int], ordering_rules: List[OrderingRule]
    ):
        self.page_list: List[int] = page_list
        self.in_correct_order: bool = self._follows_all_rules(ordering_rules)

    def __len__(self):
        return len(self.page_list)

    def __str__(self):
        return str(self.page_list)

    def get_middle_item(self) -> int:
        """Return the middle item of this PageList."""
        return get_middle(self.page_list)

    def swap(self, first_index: int, second_index: int) -> None:
        """Swap the element at first_index in the page list with the element at
        second_index.
        """
        temp = self.page_list[first_index]
        self.page_list[first_index] = self.page_list[second_index]
        self.page_list[second_index] = temp

    def _follows_all_rules(
        self, all_ordering_rules: List[OrderingRule]
    ) -> bool:
        """Return True if this PageList follows all specified ordering rules,
        False otherwise.
        """
        for rule in all_ordering_rules:
            if not self._follows_rule(rule):
                return False
        return True

    def _follows_rule(self, ordering_rule: OrderingRule) -> bool:
        """Return True if this PageList follows the specified ordering rule,
        False otherwise.
        """
        if (ordering_rule.first_page not in self.page_list) or (
            ordering_rule.second_page not in self.page_list
        ):
            # Rule does not apply to this list
            return True

        first_page_index = self.page_list.index(ordering_rule.first_page)
        # Ensure second page of rule does not appear before the first page
        for idx in range(first_page_index):
            if self.page_list[idx] == ordering_rule.second_page:
                return False
        return True


class ProblemInput:
    """Represents a problem input for Advent of Code 2024, day 5."""

    def __init__(self, file_contents: str):
        self.ordering_rules: List[OrderingRule] = []
        self.page_lists: List[PageList] = []
        # Call other functions to initialise the values of properties
        self._init_all(file_contents)

    def solve_part_one(self):
        """Add up the middle page number from each correctly-ordered page list,
        and return the result.
        """
        output = 0
        for page_list in self.page_lists:
            if page_list.in_correct_order:
                output += page_list.get_middle_item()
        return output

    def solve_part_two(self):
        """Add up the middle page numbers after correctly ordering the
        incorrectly-ordered updates, and return the result.
        """
        output = 0

        for page_list in self.page_lists:
            if not page_list.in_correct_order:
                sorted_page_list = merge_sort_page_list(
                    page_list.page_list, self.ordering_rules
                )
                output += get_middle(sorted_page_list)

        return output

    def print(self) -> None:
        """Print this problem input, for debugging purposes."""
        print("Ordering rules: ")
        self.print_ordering_rules()
        print("\nPage lists: ")
        self.print_page_lists()

    def print_ordering_rules(self) -> None:
        """Print the ordering rules of this problem input, for debugging
        purposes.
        """
        for rule in self.ordering_rules:
            print(rule)

    def print_page_lists(self) -> None:
        """Print the page lists of this problem input, for debugging
        purposes.
        """
        for page_list in self.page_lists:
            print(page_list)

    def _init_all(self, input_file_contents: str) -> None:
        self._init_ordering_rules(input_file_contents)
        self._init_page_lists(input_file_contents)

    def _init_ordering_rules(self, input_file_contents: str) -> None:
        """Extract the list of page ordering rules from the contents of the
        input file.
        """
        ordering_rules_as_strs = (input_file_contents.split("\n\n")[0]).split(
            "\n"
        )
        for rule in ordering_rules_as_strs:
            [first_page, second_page] = rule.split("|")
            self.ordering_rules.append(
                OrderingRule(int(first_page), int(second_page))
            )

    def _init_page_lists(self, input_file_contents: str) -> None:
        """Given the input file contents, extract the list of pages to produce
        in each update.

        Should be called after self.ordering_rules is initialised.
        """
        page_lists_as_strs = (input_file_contents.split("\n\n")[1]).split("\n")
        for a_list in page_lists_as_strs:
            self.page_lists.append(
                PageList(
                    string_list_to_ints(a_list.split(",")), self.ordering_rules
                )
            )


def string_list_to_ints(string_list: List) -> List:
    """Convert a list of strings to a list of integers and return."""
    output = []
    for item in string_list:
        output.append(int(item))
    return output


def merge_sort_page_list(
    a_list: List[int], ordering_rules: List[OrderingRule]
):
    # Base case. A list of zero or one elements is sorted, by definition.
    if len(a_list) <= 1:
        return a_list

    # Recursive case
    left, right = split_list_in_half(a_list)
    # Recursively sort both sublists
    left = merge_sort_page_list(left, ordering_rules)
    right = merge_sort_page_list(right, ordering_rules)
    # Merge sorted sublists
    return merge_page_list(left, right, ordering_rules)


def split_list_in_half(a_list: List[int]):
    half_list_size = len(a_list) // 2
    return a_list[:half_list_size], a_list[half_list_size:]


def merge_page_list(
    left: List[int], right: List[int], ordering_rules: List[OrderingRule]
):
    result = []
    while len(left) > 0 and len(right) > 0:
        if should_occur_before(left[0], right[0], ordering_rules):
            result.append(left[0])
            left.pop(0)
        else:
            result.append(right[0])
            right.pop(0)
    # Either left or right may have elements left; consume them
    while len(left) > 0:
        result.append(left[0])
        left.pop(0)
    while len(right) > 0:
        result.append(right[0])
        right.pop(0)
    return result


def should_occur_before(a: int, b: int, ordering_rules: List[OrderingRule]):
    """Return True if `a` should appear before `b` based on the given
    OrderingRules, False otherwise.
    """
    for ordering_rule in ordering_rules:
        if ordering_rule.contains(a) and ordering_rule.contains(b):
            return a == ordering_rule.first_page


def get_middle(a_list: List[int]) -> int:
    middle_index = int((len(a_list) - 1) / 2)
    return a_list[middle_index]
