from enum import Enum


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    TOP_RIGHT = 5
    BOTTOM_RIGHT = 6
    TOP_LEFT = 7
    BOTTOM_LEFT = 8


class SearchPath:
    """Defines a linear search path for the XMAS word search."""

    def __init__(self, direction: Direction):
        """Initialise this SearchPath with a direction, and how much the row
        and column should be incremented in each step of the search.

        Args:
            direction (Direction)
        """
        self.direction = direction
        self.row_increment: int = None
        self.col_increment: int = None
        self._init_row_increment()
        self._init_col_increment()

    def _init_row_increment(self):
        """Initialise self.row_increment with how much the row should be
        incremented with each step of the search.
        """
        if self.direction in [
            Direction.UP,
            Direction.TOP_LEFT,
            Direction.TOP_RIGHT,
        ]:
            self.row_increment = -1
            return
        if self.direction in [
            Direction.DOWN,
            Direction.BOTTOM_LEFT,
            Direction.BOTTOM_RIGHT,
        ]:
            self.row_increment = 1
            return
        self.row_increment = 0

    def _init_col_increment(self):
        """Initialise self.col_increment with how much the column should be
        incremented with each step of the search.
        """
        if self.direction in [
            Direction.LEFT,
            Direction.BOTTOM_LEFT,
            Direction.TOP_LEFT,
        ]:
            self.col_increment = -1
            return
        if self.direction in [
            Direction.RIGHT,
            Direction.BOTTOM_RIGHT,
            Direction.TOP_RIGHT,
        ]:
            self.col_increment = 1
            return
        self.col_increment = 0
