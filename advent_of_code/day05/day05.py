"""
Solution for Advent of Code 2024, day 5.
"""

from dataclasses import dataclass
from typing import List
from advent_of_code.util import print_output_string, file_contents_as_string

INPUT_FILEPATH = "advent_of_code/day05/input_day05.txt"


@dataclass
class OrderingRule:
    """A page ordering rule. Indicates that the `first_page` must be printed
    at some point before the `second_page` in all updates.
    """

    first_page: int
    second_page: int

    def __str__(self):
        return f"{self.first_page}|{self.second_page}"


@dataclass
class PageList:
    """Pages to print in a given update."""

    page_list: List[int]

    def __len__(self):
        return len(self.page_list)

    def __str__(self):
        return str(self.page_list)

    def follows_all_rules(self, all_ordering_rules: List[OrderingRule]):
        """Return True if this PageList follows all specified ordering rules,
        False otherwise.
        """
        for rule in all_ordering_rules:
            if not self._follows_rule(rule):
                return False
        return True

    def _follows_rule(self, ordering_rule: OrderingRule):
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

    def get_middle_item(self):
        """Return the middle item of this PageList."""
        middle_index = int((len(self.page_list) - 1) / 2)
        return self.page_list[middle_index]


class ProblemInput:
    def __init__(self, file_contents: str):
        self.ordering_rules: List[OrderingRule] = []
        self.page_lists: List[PageList] = []
        # Call other functions to initialise the values of properties
        self._init_ordering_rules(file_contents)
        self._init_page_lists(file_contents)

    def solve_part_one(self):
        """Add up the middle page number from each correctly-ordered page list
        and return.
        """
        output = 0
        for page_list in self.page_lists:
            if page_list.follows_all_rules(self.ordering_rules):
                output += page_list.get_middle_item()
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
        in each update."""
        page_lists_as_strs = (input_file_contents.split("\n\n")[1]).split("\n")
        for a_list in page_lists_as_strs:
            self.page_lists.append(
                PageList(string_list_to_ints(a_list.split(",")))
            )


def main() -> None:
    """Compute and print the solution to Advent of Code 2024, day 5."""
    print_output_string(5, 1)
    problem_input = ProblemInput(file_contents_as_string(INPUT_FILEPATH))
    print(problem_input.solve_part_one())


def string_list_to_ints(string_list: List) -> List:
    """Convert a list of strings to a list of integers and return."""
    output = []
    for item in string_list:
        output.append(int(item))
    return output
