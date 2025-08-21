from __future__ import annotations
from typing import List

class InsertionSort:
    """Insertion Sort (stable): O(n^2) worst/avg, O(n) best for nearly-sorted data."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        a = arr[:]
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1
            while j >= 0 and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key
        return a

def main() -> None:
    data = [12, 11, 13, 5, 6]
    print("Input :", data)
    print("Sorted:", InsertionSort.sort(data))

if __name__ == "__main__":
    main()
