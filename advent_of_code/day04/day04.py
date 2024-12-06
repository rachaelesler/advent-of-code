from advent_of_code import util
from advent_of_code.day04.part1 import count_xmas_in_wordsearch


INPUT_FILEPATH = "advent_of_code/day04/input_day04.txt"


def main() -> None:
    wordsearch_arr = wordsearch_file_to_array(INPUT_FILEPATH)

    util.print_output_string(4, 1)
    print(count_xmas_in_wordsearch(wordsearch_arr))


def wordsearch_file_to_array(filepath: str):
    wordsearch = []
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        # Interpret each line as an array
        for line in file:
            line = line.strip("\n")
            wordsearch.append(list(line))
    return wordsearch
