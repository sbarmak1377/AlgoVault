from __future__ import annotations
from typing import List

class SelectionSort:
    """Selection Sort (unstable): O(n^2) time, O(1) extra space."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        a = arr[:]
        n = len(a)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if a[j] < a[min_idx]:
                    min_idx = j
            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]
        return a

def main() -> None:
    data = [64, 25, 12, 22, 11]
    print("Input :", data)
    print("Sorted:", SelectionSort.sort(data))

if __name__ == "__main__":
    main()
