"""Functions for performing top-down merge sort.
Based on pseudocode at https://en.wikipedia.org/wiki/Merge_sort
"""

from typing import List


def merge_sort(a_list: List[int]) -> List[int]:
    # Base case. A list of zero or one elements is sorted, by definition.
    if len(a_list) <= 1:
        return a_list

    # Recursive case
    left, right = split_list_in_half(a_list)
    # Recursively sort both sublists
    left = merge_sort(left)
    right = merge_sort(right)
    # Merge sorted sublists
    return merge(left, right)


def split_list_in_half(a_list: List[int]):
    half_list_size = len(a_list) // 2
    return a_list[:half_list_size], a_list[half_list_size:]


def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    while len(left) > 0 and len(right) > 0:
        if left[0] <= right[0]:
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


if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6, 7]
    print("Given array is")
    print(arr)
    sorted_arr = merge_sort(arr)
    print("Sorted array is")
    print(sorted_arr)
