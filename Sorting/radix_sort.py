from __future__ import annotations
from typing import List

class RadixSort:
    """LSD Radix Sort (base 10) for non-negative integers. Stable; O(d*(n + b))."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        if not arr:
            return []
        if min(arr) < 0:
            raise ValueError("RadixSort expects non-negative integers.")
        a = arr[:]
        exp = 1  # 1, 10, 100, ...
        max_val = max(a)
        while max_val // exp > 0:
            a = RadixSort._counting_pass(a, exp)
            exp *= 10
        return a

    @staticmethod
    def _counting_pass(a: List[int], exp: int) -> List[int]:
        count = [0] * 10
        for x in a:
            digit = (x // exp) % 10
            count[digit] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        out = [0] * len(a)
        for x in reversed(a):  # stable
            digit = (x // exp) % 10
            count[digit] -= 1
            out[count[digit]] = x
        return out

def main() -> None:
    data = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Input :", data)
    print("Sorted:", RadixSort.sort(data))

if __name__ == "__main__":
    main()
