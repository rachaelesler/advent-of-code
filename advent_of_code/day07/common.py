from typing import List


def load_input(filepath: str) -> List:
    output = []
    with open(
        filepath,
        encoding="utf-8",
    ) as file:
        for line in file:
            line_arr = line.split(":")
            test_val = int(line_arr[0])
            equation_vals = [int(x) for x in line_arr[1].strip().strip("\n").split(" ")]
            output.append([test_val, equation_vals])
    return output
