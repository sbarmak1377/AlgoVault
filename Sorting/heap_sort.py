from __future__ import annotations
from typing import List

class HeapSort:
    """Heap Sort (unstable): O(n log n) time, O(1) extra space (on a copy)."""

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        a = arr[:]  # we won't mutate the caller's list
        n = len(a)

        # build max-heap
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify(a, n, i)

        # extract elements
        for end in range(n - 1, 0, -1):
            a[0], a[end] = a[end], a[0]
            HeapSort._heapify(a, end, 0)
        return a

    @staticmethod
    def _heapify(a: List[int], heap_size: int, root: int) -> None:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < heap_size and a[left] > a[largest]:
            largest = left
        if right < heap_size and a[right] > a[largest]:
            largest = right
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            HeapSort._heapify(a, heap_size, largest)

def main() -> None:
    data = [12, 11, 13, 5, 6, 7]
    print("Input :", data)
    print("Sorted:", HeapSort.sort(data))

if __name__ == "__main__":
    main()
