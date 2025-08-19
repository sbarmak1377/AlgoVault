from typing import List
def linear_search(arr: List, target: int) -> int:
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def binary_search(arr: List, target: int) -> int:
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def main():
    nums_unsorted = [7, 2, 9, 4, 1]
    nums_sorted = [1, 2, 4, 7, 9]

    print(linear_search(nums_unsorted, 4))
    print(binary_search(nums_unsorted, 4))
    print(binary_search(nums_sorted, 4))  # → 2
    print(binary_search(nums_sorted, 8))  # → -1


if __name__ == '__main__':
    main()