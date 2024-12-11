"""
Solution for Advent of Code 2024, day 5.

The problem involves counting how many positions a security guard will visit
in their patrol.
"""

from typing import List
from advent_of_code.util import print_output_string

INPUT_FILEPATH = "advent_of_code/day06/input_day06.txt"
INPUT_FILEPATH_SMALL = "advent_of_code/day06/input_day06_small.txt"


def main() -> None:
    """Compute and print the solution to Advent of Code 2024, day 5."""
    print_output_string(6, 1)
    my_map = MapArea(INPUT_FILEPATH_SMALL)
    my_map.traverse()
    print(my_map.count_visited_positions())


class MapArea:

    OBSTRUCTION = "#"
    GUARD_ORIENTATIONS = ["^", "V", "<", ">"]

    def __init__(self, filepath: str):
        self.map_area = []
        self.current_row = -1
        self.current_col = -1
        self._initialise(filepath)

    def _initialise(self, filepath: str):
        with open(
            filepath,
            encoding="utf-8",
        ) as file:
            for line in file:
                self.map_area.append(list(line.strip("\n")))

        self.current_row, self.current_col = self.get_current_position()

    def get_current_position(self):
        """Get the current position (row and column) of the guard on the
        map.
        """
        n_rows = len(self.map_area)
        for row in range(n_rows):
            n_cols = len(self.map_area[row])
            for col in range(n_cols):
                if self.is_valid_orientation(self.map_area[row][col]):
                    return row, col
        raise ValueError("Guard not found")

    def get_current_cursor(self):
        orientation = self.map_area[self.current_row][self.current_col]
        if self.is_valid_orientation(orientation):
            return orientation
        raise ValueError("Current orientation is invalid")

    def is_valid_orientation(self, orientation: str) -> bool:
        return orientation in self.GUARD_ORIENTATIONS

    def set_current_cursor(self, new_cursor: str):
        self.map_area[self.current_row][self.current_col] = new_cursor

    def turn_right(self):
        orientation = self.get_current_cursor()
        match orientation:
            case "^":
                self.set_current_cursor(">")
                return
            case ">":
                self.set_current_cursor("V")
                return
            case "V":
                self.set_current_cursor("<")
                return
            case "<":
                self.set_current_cursor("^")
                return
            case _:
                raise ValueError("Error turning right")

    def get_next_position(self):
        raise NotImplementedError()

    def move_to_next_position(self):
        raise NotImplementedError()

    def is_next_position_an_obstacle(self):
        raise NotImplementedError()

    def is_next_position_off_map(self):
        raise NotImplementedError()

    def mark_position_as_visited(self):
        raise NotImplementedError()

    def traverse(self):
        raise NotImplementedError()

    def count_visited_positions(self):
        raise NotImplementedError()
