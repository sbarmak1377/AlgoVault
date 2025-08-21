from __future__ import annotations
from typing import List

class BucketSort:
    """
    Bucket Sort for floats in [0, 1).
    Distributes values into buckets, sorts each (using insertion sort), concatenates.
    """

    @staticmethod
    def sort(arr: List[float], bucket_count: int | None = None) -> List[float]:
        if not arr:
            return []
        n = len(arr)
        if bucket_count is None:
            bucket_count = n  # typical choice
        buckets: List[List[float]] = [[] for _ in range(bucket_count)]
        for x in arr:
            if not (0.0 <= x < 1.0):
                raise ValueError("BucketSort expects floats in [0, 1).")
            idx = int(x * bucket_count)
            buckets[idx].append(x)
        # sort each bucket with insertion sort
        def insertion(a: List[float]) -> List[float]:
            for i in range(1, len(a)):
                key = a[i]
                j = i - 1
                while j >= 0 and a[j] > key:
                    a[j + 1] = a[j]
                    j -= 1
                a[j + 1] = key
            return a
        out: List[float] = []
        for b in buckets:
            out.extend(insertion(b))
        return out

def main() -> None:
    data = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print("Input :", data)
    print("Sorted:", BucketSort.sort(data))

if __name__ == "__main__":
    main()
