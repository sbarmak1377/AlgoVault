from __future__ import annotations
from typing import List

class ShellSort:
    """Shell Sort using halving gap sequence. In-place; avg ~O(n^{3/2}) depending on gaps."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        a = arr[:]
        n = len(a)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = a[i]
                j = i
                while j >= gap and a[j - gap] > temp:
                    a[j] = a[j - gap]
                    j -= gap
                a[j] = temp
            gap //= 2
        return a

def main() -> None:
    data = [23, 12, 1, 8, 34, 54, 2, 3]
    print("Input :", data)
    print("Sorted:", ShellSort.sort(data))

if __name__ == "__main__":
    main()
