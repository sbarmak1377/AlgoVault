from __future__ import annotations
from typing import List

class BubbleSort:
    """Bubble Sort (stable): O(n^2) worst/avg, O(n) best when already sorted."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        a = arr[:]  # work on a copy (functional style)
        n = len(a)
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swapped = True
            if not swapped:
                break
        return a

def main() -> None:
    data = [5, 1, 4, 2, 8, 0, 2]
    print("Input :", data)
    print("Sorted:", BubbleSort.sort(data))

if __name__ == "__main__":
    main()
