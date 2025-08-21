from __future__ import annotations
from typing import List

class MergeSort:
    """Merge Sort (stable): O(n log n) time, O(n) space. Returns a new sorted list."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr[:]
        mid = len(arr) // 2
        left = MergeSort.sort(arr[:mid])
        right = MergeSort.sort(arr[mid:])
        return MergeSort._merge(left, right)

    @staticmethod
    def _merge(left: List[int], right: List[int]) -> List[int]:
        result: List[int] = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

def main() -> None:
    data = [38, 27, 43, 3, 9, 82, 10]
    print("Input :", data)
    print("Sorted:", MergeSort.sort(data))

if __name__ == "__main__":
    main()
