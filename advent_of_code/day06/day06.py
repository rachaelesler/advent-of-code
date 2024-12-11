"""
Solution for Advent of Code 2024, day 5.

The problem involves counting how many positions a security guard will visit
in their patrol.
"""

from typing import TypedDict
from advent_of_code.util import print_output_string

INPUT_FILEPATH = "advent_of_code/day06/input_day06.txt"
INPUT_FILEPATH_SMALL = "advent_of_code/day06/input_day06_small.txt"


def main() -> None:
    """Compute and print the solution to Advent of Code 2024, day 5."""
    print_output_string(6, 1)
    my_map = MapArea(INPUT_FILEPATH)
    output = my_map.traverse_and_return_count()
    # print(my_map)
    print(output)


class Position(TypedDict):
    row: int
    col: int


class CursorConfig(TypedDict):
    cursor: str
    next_cursor: str
    next_position_increment: Position


class GuardOrientation(TypedDict):
    up: CursorConfig
    down: CursorConfig
    left: CursorConfig
    right: CursorConfig


class MapArea:
    """Represents puzzle input and solution."""

    OBSTRUCTION = "#"
    VISITED = "X"
    UNVISITED = "."

    guard_direction_data: GuardOrientation = {
        "up": {
            "cursor": "^",
            "next_cursor": ">",
            "next_position_increment": {"row": -1, "col": 0},
        },
        "down": {
            "cursor": "V",
            "next_cursor": "<",
            "next_position_increment": {"row": 1, "col": 0},
        },
        "left": {
            "cursor": "<",
            "next_cursor": "^",
            "next_position_increment": {"row": 0, "col": -1},
        },
        "right": {
            "cursor": ">",
            "next_cursor": "V",
            "next_position_increment": {"row": 0, "col": 1},
        },
    }

    def __init__(self, filepath: str):
        self.map_area = []
        self.curr_row = -1
        self.curr_col = -1
        self._initialise(filepath)

    def __str__(self):
        output = ""
        for row in self.map_area:
            output += "".join(row) + "\n"
        return output

    def _initialise(self, filepath: str):
        """Initialise this MapArea.

        Should only be called in the __init__() function.
        """
        with open(
            filepath,
            encoding="utf-8",
        ) as file:
            for line in file:
                self.map_area.append(list(line.strip("\n")))

        self.curr_row, self.curr_col = self.current_position

    @property
    def valid_cursors(self):
        return [
            val["cursor"] for key, val in self.guard_direction_data.items()
        ]

    @property
    def current_position(self):
        """Get the current position (row and column) of the guard on the
        map.
        """
        n_rows = len(self.map_area)
        for row in range(n_rows):
            n_cols = len(self.map_area[row])
            for col in range(n_cols):
                if self.is_valid_cursor(self.map_area[row][col]):
                    return row, col
        raise ValueError("Guard not found")

    @property
    def current_cursor(self) -> str:
        """Return the current "cursor" of the security guard
        (that is, one of ^, <, >, or V).

        Raises a ValueError if the current position represented by this MapArea
        does not correspond to the guard's position.
        """
        orientation = self.map_area[self.curr_row][self.curr_col]
        if self.is_valid_cursor(orientation):
            return orientation
        raise ValueError("Current orientation is invalid")

    def is_valid_cursor(self, cursor: str) -> bool:
        """Return True if the specified cursor is valid, False otherwise."""
        return cursor in self.valid_cursors

    def set_current_cursor(self, new_cursor: str):
        """Set the current cursor to be the new cursor."""
        self.map_area[self.curr_row][self.curr_col] = new_cursor

    def turn_right(self) -> None:
        """Turn the cursor of the guard 90 degrees clockwise."""
        config: CursorConfig = self.get_cursor_config()
        self.set_current_cursor(config["next_cursor"])

    def get_cursor_config(self) -> CursorConfig:
        """Get the config for the current cursor."""
        cursor = self.current_cursor
        for key, val in self.guard_direction_data.items():
            if val["cursor"] == cursor:
                return val
        raise ValueError("Error getting cursor config")

    def is_position_off_map(self, row: int, col: int):
        """Return True if the position indicated by the specified row and
        column is outside the boundaries of the map, False otherwise.
        """
        return (
            row < 0
            or col < 0
            or row >= len(self.map_area)
            or col >= len(self.map_area[0])
        )

    def mark_position_as_visited(self, row: int, col: int) -> None:
        self.map_area[row][col] = self.VISITED

    def traverse_and_return_count(self) -> int:
        unique_visited_positions = 1
        next_row, next_col = self.get_next_position()
        # print("\nRow\tCol\tCursor\t")

        while not self.is_position_off_map(next_row, next_col):
            # print(f"{next_row}\t{next_col}\t{self.current_cursor}")
            next_symbol = self.map_area[next_row][next_col]
            cursor = self.current_cursor
            if next_symbol == self.OBSTRUCTION:
                # When the guard reaches an obstruction, turn right
                # Do not change current position
                self.turn_right()
            elif next_symbol == self.UNVISITED:
                # Guard reaches an unvisited position
                # Increment count and move to next position
                unique_visited_positions += 1
                self.map_area[self.curr_row][self.curr_col] = self.VISITED
                self.map_area[next_row][next_col] = cursor
                self.curr_row = next_row
                self.curr_col = next_col
            elif next_symbol == self.VISITED:
                # Guard reaches an already-visited position
                # Move to next position without incrementing count
                self.map_area[self.curr_row][self.curr_col] = self.VISITED
                self.map_area[next_row][next_col] = cursor
                self.curr_row = next_row
                self.curr_col = next_col
            else:
                raise ValueError(
                    f"Invalid symbol detected at {next_row}, {next_col}: "
                    + f"{next_symbol}"
                )
            next_row, next_col = self.get_next_position()

        # When execution reaches here, the guard has moved off the map
        self.mark_position_as_visited(self.curr_row, self.curr_col)
        return unique_visited_positions

    def get_next_position(self):
        config: CursorConfig = self.get_cursor_config()
        # print("Next position function")
        # print(config["next_position_increment"]["row"])
        next_row = self.curr_row + config["next_position_increment"]["row"]
        next_col = self.curr_col + config["next_position_increment"]["col"]
        return next_row, next_col
