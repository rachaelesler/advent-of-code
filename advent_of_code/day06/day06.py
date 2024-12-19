"""
Solution for Advent of Code 2024, day 5.

The problem involves counting how many positions a security guard will visit
in their patrol.
"""

from typing import List, TypedDict

from advent_of_code.util import print_output_string

INPUT_FILEPATH = "advent_of_code/day06/input_day06.txt"
INPUT_FILEPATH_SMALL = "advent_of_code/day06/input_day06_small.txt"


def main() -> None:
    """Compute and print the solution to Advent of Code 2024, day 5."""
    map_area = MapArea(INPUT_FILEPATH)

    # Part one
    print_output_string(6, 1)
    map_area.traverse()
    print(map_area.unique_visited_positions)

    # Part two
    print_output_string(6, 2)
    map_area = MapArea(INPUT_FILEPATH)
    map_area.solve_part_two(False)
    print(map_area.good_obstacle_positions)


class Position(TypedDict):
    """Represents a position on the map area (row and column)."""

    row: int
    col: int


class CursorConfig(TypedDict):
    """Represents a cursor (symbol that represents which direction the guard is
    facing), the "next" cursor (how the cursor will look when rotated to the
    right 90 degrees), and the "next position increment" (how much to add to
    the current row/column when moving to the next position).
    """

    cursor: str
    next_cursor: str
    next_position_increment: Position


class GuardOrientation(TypedDict):
    """Represents the config for the guard when they are facing in a particular
    direction.
    """

    up: CursorConfig
    down: CursorConfig
    left: CursorConfig
    right: CursorConfig


class MapArea:
    """Represents puzzle input and solution."""

    OBSTRUCTION = "#"
    NEW_OBSTRUCTION = "0"
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
        # Store current map area, guard position, and positions guard has visited
        self.map_area: List[List[str]] = []
        # Original map area
        self.original_map_area: List[List[str]] = []
        # Store current position
        self.curr_row = -1
        self.curr_col = -1
        self._initialise(filepath)
        # Store where guard started
        self.starting_row = self.curr_row
        self.starting_col = self.curr_col
        # Store original cursor
        self.original_cursor = self.map_area[self.curr_row][self.curr_col]
        # Count how many unique positions were visited in this "run"
        self.unique_visited_positions = 1
        # Cumulative count of how many positions we could put an obstacle in,
        # that would result in the guard being stuck in a loop
        self.good_obstacle_positions = 0
        # Possible obstacle positions is a list of (row, column) tuples
        self.possible_obstacle_positions: List = []

        # self.visited_position_history represents a grid that is the same size
        # as the map area. It stores the cursor we used when we visited each
        # position.
        self.visited_position_history: List = []
        for row_idx in range(len(self.map_area)):
            self.visited_position_history.append([[] for _ in range(len(self.map_area[row_idx]))])

    def __str__(self):
        output = ""
        for row in self.map_area:
            output += "".join(row) + "\n"
        return output

    def _initialise(self, filepath: str) -> None:
        """Initialise this MapArea.

        Should only be called in the __init__() function.
        """
        with open(
            filepath,
            encoding="utf-8",
        ) as file:
            for line in file:
                row = list(line.strip("\n"))
                self.map_area.append(row)
                self.original_map_area.append(row)

        self.curr_row, self.curr_col = self.current_position

    def reset(self) -> None:
        """Set the map area back to its original state.
        Reset the list of visited positions so it is empty.
        Set the count of unique visited positions to 1.
        """
        self.reset_map()
        self.unique_visited_positions = 1
        self.visited_position_history = []
        self.curr_row = self.starting_row
        self.curr_col = self.starting_col
        self.map_area[self.starting_row][self.starting_col] = self.original_cursor
        for row_idx in range(len(self.map_area)):
            self.visited_position_history.append([[] for _ in range(len(self.map_area[row_idx]))])

    def reset_map(self) -> None:
        """Reset the map back to its original state."""
        n_rows = len(self.map_area)
        for row_idx in range(n_rows):
            n_cols = len(self.map_area[row_idx])
            for col_idx in range(n_cols):
                if self.map_area[row_idx][col_idx] != self.OBSTRUCTION:
                    self.map_area[row_idx][col_idx] = self.UNVISITED

    @property
    def valid_cursors(self) -> List:
        """Return a list of valid "cursors" (that is, ways of displaying the
        guard's current position).
        """
        return [val["cursor"] for key, val in self.guard_direction_data.items()]

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
        for _, val in self.guard_direction_data.items():
            if val["cursor"] == cursor:
                return val
        raise ValueError("Error getting cursor config")

    def is_position_off_map(self, row: int, col: int):
        """Return True if the position indicated by the specified row and
        column is outside the boundaries of the map, False otherwise.
        """
        return row < 0 or col < 0 or row >= len(self.map_area) or col >= len(self.map_area[0])

    def mark_position_as_visited(self, row: int, col: int) -> None:
        """Mark the position on the map at the specified row and column with an
        "X" to indicate it has been visited.
        """
        self.map_area[row][col] = self.VISITED

    def move_forward(self, cursor: str, next_row: int, next_col: int):
        """Mark the current position as visited.
        Move the guard to the position indicated by next_row, next_col.
        """
        # Ensure next position is not an obstacle
        if self.is_position_obstruction(next_row, next_col):
            raise ValueError("Cannot move forward when there is an obstruction")

        # Set current position as visited
        self.map_area[self.curr_row][self.curr_col] = self.VISITED
        # Add the current position to the list of already-visited positions
        self.visited_position_history[self.curr_row][self.curr_col].append(cursor)
        # Set the next position as the cursor
        self.map_area[next_row][next_col] = cursor
        self.curr_row = next_row
        self.curr_col = next_col

    def traverse(self, interactive=False) -> bool:
        """Return True if the guard would exit the map with the current map
        area and configuration, False if the path would contain cycles.

        Simulate the guard moving completely through the map area based on
        the rules defined in the puzzle.
        """
        next_row, next_col = self.get_next_position()
        iters = 0

        while not self.is_position_off_map(next_row, next_col):
            iters += 1
            if iters > 10000:
                return False
            if interactive:
                print(self)
                input()
            next_symbol = self.map_area[next_row][next_col]
            cursor = self.current_cursor

            if self.is_position_obstruction(next_row, next_col):
                # When the guard reaches an obstruction, turn right
                # Do not change current position
                self.turn_right()
            elif next_symbol == self.UNVISITED:
                # Guard reaches an unvisited position
                # Increment count and move to next position
                self.unique_visited_positions += 1
                self.move_forward(cursor, next_row, next_col)
            elif next_symbol == self.VISITED:
                # Guard reaches an already-visited position:

                # Check if we have already been there with the current
                # orientation before
                previous_cursors_at_next_pos = self.visited_position_history[next_row][next_col]
                for previous_cursor in previous_cursors_at_next_pos:
                    if cursor == previous_cursor:
                        # We have reached the current position with the same
                        # orientation before -> stuck in a loop
                        return False

                # Move to next position without incrementing count
                self.move_forward(cursor, next_row, next_col)
            else:
                raise ValueError(
                    f"Invalid symbol detected at {next_row}, {next_col}: " + f"{next_symbol}"
                )
            next_row, next_col = self.get_next_position()

        # When execution reaches here, the guard has moved off the map
        self.mark_position_as_visited(self.curr_row, self.curr_col)
        return True

    def get_next_position(self):
        """Get the next row and column that the guard should move to, based on
        the current row and column and the current cursor.
        """
        config: CursorConfig = self.get_cursor_config()
        next_row = self.curr_row + config["next_position_increment"]["row"]
        next_col = self.curr_col + config["next_position_increment"]["col"]
        return next_row, next_col

    def add_obstruction(self, row: int, col: int) -> None:
        """Add a new obstruction at the specified row and column."""
        self.map_area[row][col] = self.NEW_OBSTRUCTION

    def solve_part_two(self, debug=False, interactive=False):
        """Return a count of the number of positions we could place an obstacle
        on that would result in the guard moving in a cycle.
        """
        # Only try putting an obstacle on positions in the guard's original path
        possible_obstacle_positions = self.get_possible_obstacle_positions()
        for obstacle_pos in possible_obstacle_positions:
            row_idx = obstacle_pos[0]
            col_idx = obstacle_pos[1]

            if row_idx == self.starting_row and col_idx == self.starting_col:
                # Don't place an obstacle at the guard's start position
                continue
            self.add_obstruction(row_idx, col_idx)
            if debug:
                print(f"Obstacle at {row_idx}, {col_idx}")
                print(self)
                print()
            can_traverse = self.traverse(interactive)
            if not can_traverse:
                self.good_obstacle_positions += 1
            # Reset map and visited position history
            self.reset()

    def is_position_obstruction(self, row: int, col: int) -> bool:
        return (
            self.map_area[row][col] == self.OBSTRUCTION
            or self.map_area[row][col] == self.NEW_OBSTRUCTION
        )

    def get_possible_obstacle_positions(self):
        # Possible obstacle positions is a list of (row, column) tuples
        output = []
        self.reset()
        self.traverse()
        # Iterate through each position in map
        n_rows = len(self.map_area)
        n_cols = len(self.map_area[0])
        for row_idx in range(n_rows):
            for col_idx in range(n_cols):
                if self.map_area[row_idx][col_idx] == self.VISITED:
                    pos = (row_idx, col_idx)
                    output.append(pos)
        self.reset()
        return output
