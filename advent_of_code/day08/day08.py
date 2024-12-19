"""
Advent of Code 2024, day 8.
"""

import numpy as np
import numpy.typing as npt

from advent_of_code.util import print_output_string

INPUT_FILEPATH = "advent_of_code/day08/input.txt"
INPUT_FILEPATH_SMALL = "advent_of_code/day08/input_small.txt"
INPUT_FILEPATH_TINY = "advent_of_code/day08/input_tiny.txt"

DEFAULT_CHARACTER = "."
ANTINODE = "#"


def main():
    """Print the solutions."""
    print_output_string(8, 1)

    solution = solve_part_one(INPUT_FILEPATH_TINY)
    print("\n\n")
    print(solution)


def load_input(filepath: str) -> np.array:
    """Load the problem from the text file at specified filepath into a NumPy array and return."""
    output = []
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        for line in file:
            output.append(list(line.strip("\n")))
    return np.array(output)


def solve_part_one(filepath: str) -> int:
    output = 0
    # Frequency map
    freq_map = load_input(filepath)
    # Unique alphanumeric character "frequencies" in map (with "." removed)
    unique_chars = delete_by_value(np.unique(freq_map), DEFAULT_CHARACTER)
    # For each symbol, find their position (row, column)
    for char in unique_chars.flat:
        # Find where they occur on the map
        print(char)
        locations = np.argwhere(freq_map == char)
        # For each location, place an antinode based on the other locations
        for i in range(locations.shape[0]):
            for j in range(i + 1, locations.shape[0]):
                diff = locations[i] - locations[j]
                antinode_1 = locations[i] + diff
                antinode_2 = locations[j] - diff
                print(f"Antinode locations: {antinode_1} {antinode_2}")
                # print(locations[i] - locations[j])
                place_antinode(freq_map, antinode_1)
                print(freq_map)
                # place_antinode(freq_map, antinode_1)

    return output


def delete_by_value(arr, val) -> npt.NDArray:
    index = np.argwhere(arr == val)
    return np.delete(arr, index)


def place_antinode(freq_map, position) -> bool:
    row_idx, col_idx = position
    n_rows, n_cols = freq_map.shape
    if row_idx <= 0 or col_idx <= 0 or row_idx >= n_rows or col_idx >= n_cols:
        return False
    freq_map[row_idx, col_idx] = ANTINODE
    return True
