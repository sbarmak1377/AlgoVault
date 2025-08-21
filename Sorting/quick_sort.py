from __future__ import annotations
from typing import List

class QuickSort:
    """Quick Sort (unstable): Avg O(n log n), worst O(n^2). Uses Lomuto partition on a copy."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        a = arr[:]
        QuickSort._quicksort(a, 0, len(a) - 1)
        return a

    @staticmethod
    def _quicksort(a: List[int], lo: int, hi: int) -> None:
        if lo < hi:
            p = QuickSort._partition(a, lo, hi)
            QuickSort._quicksort(a, lo, p - 1)
            QuickSort._quicksort(a, p + 1, hi)

    @staticmethod
    def _partition(a: List[int], lo: int, hi: int) -> int:
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        return i

def main() -> None:
    data = [10, 7, 8, 9, 1, 5]
    print("Input :", data)
    print("Sorted:", QuickSort.sort(data))

if __name__ == "__main__":
    main()
