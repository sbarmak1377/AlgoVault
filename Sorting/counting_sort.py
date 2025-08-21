from __future__ import annotations
from typing import List

class CountingSort:
    """
    Counting Sort for non-negative integers with reasonable max value.
    Stable version.
    """

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        if not arr:
            return []
        if min(arr) < 0:
            raise ValueError("CountingSort expects non-negative integers.")
        k = max(arr)
        count = [0] * (k + 1)
        for x in arr:
            count[x] += 1
        # prefix sums
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        out = [0] * len(arr)
        # build output (stable)
        for x in reversed(arr):
            count[x] -= 1
            out[count[x]] = x
        return out

def main() -> None:
    data = [4, 2, 2, 8, 3, 3, 1]
    print("Input :", data)
    print("Sorted:", CountingSort.sort(data))

if __name__ == "__main__":
    main()
