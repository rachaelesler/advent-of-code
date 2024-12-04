"""HistorianList class for Advent of Code 2024."""


class HistorianList:
    """Class to keep track of items in two lists."""

    def __init__(self, filepath: str):
        self.left_list = []
        self.right_list = []
        with open(
            filepath,
            encoding="utf-8",
        ) as file:
            for line in file:
                line_as_list = line.strip("\n").split()
                self.left_list.append(int(line_as_list[0]))
                self.right_list.append(int(line_as_list[1]))
        self.left_list.sort()
        self.right_list.sort()
        self._distance = None

    @property
    def length(self) -> int:
        """Get the length of this HistorianList."""
        return len(self.left_list)

    @property
    def distance(self) -> int:
        """Return the distance between the left list and the right list."""
        if self._distance is None:
            self._calculate_distance()
        return self._distance

    @property
    def similarity(self) -> int:
        """Calculate the similarity score between the left list and the right
        list.
        """
        # add up each number in the left list after multiplying it by the
        # number of times it appears in the right list.
        left_list_set = list(set(self.left_list))
        set_length = len(left_list_set)
        # Multiply each item in the left list by the number of times it appears
        # in the right list
        for i in range(set_length):
            left_list_set[i] *= self.right_list.count(left_list_set[i])
        # Sum the result
        return sum(left_list_set)

    def _calculate_distance(self):
        """Calculate the distance between the left list and the right list."""
        distance = 0
        for i in range(self.length):
            distance += abs(self.left_list[i] - self.right_list[i])
        self._distance = distance
