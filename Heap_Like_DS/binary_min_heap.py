from __future__ import annotations
from typing import List, Optional, Iterable

class BinaryMinHeap:
    """Array-based binary min-heap (priority queue)."""
    def __init__(self, items: Optional[Iterable[int]] = None) -> None:
        self.a: List[int] = []
        if items:
            self.a = list(items)
            self._heapify()

    # Core API
    def insert(self, x: int) -> None:
        self.a.append(x)
        self._sift_up(len(self.a) - 1)

    def find_min(self) -> int:
        if not self.a:
            raise IndexError("find_min from empty heap")
        return self.a[0]

    def extract_min(self) -> int:
        if not self.a:
            raise IndexError("extract_min from empty heap")
        m = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self._sift_down(0)
        return m

    def decrease_key(self, idx: int, new_key: int) -> None:
        if idx < 0 or idx >= len(self.a):
            raise IndexError("index out of range")
        if new_key > self.a[idx]:
            raise ValueError("new key is greater than current key")
        self.a[idx] = new_key
        self._sift_up(idx)

    def delete(self, idx: int) -> int:
        if idx < 0 or idx >= len(self.a):
            raise IndexError("index out of range")
        key = self.a[idx]
        self.decrease_key(idx, float('-inf'))
        self.extract_min()
        return key

    # Helpers
    def _heapify(self) -> None:
        for i in range((len(self.a) // 2) - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        while i > 0:
            p = (i - 1) // 2
            if self.a[p] <= self.a[i]:
                break
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def _sift_down(self, i: int) -> None:
        n = len(self.a)
        while True:
            l = 2 * i + 1
            r = 2 * i + 2
            smallest = i
            if l < n and self.a[l] < self.a[smallest]:
                smallest = l
            if r < n and self.a[r] < self.a[smallest]:
                smallest = r
            if smallest == i:
                break
            self.a[i], self.a[smallest] = self.a[smallest], self.a[i]
            i = smallest

def main() -> None:
    heap = BinaryMinHeap([5, 3, 8, 1, 2])
    print("Initial min:", heap.find_min())
    heap.insert(0)
    print("After insert 0, min:", heap.find_min())
    print("Extract mins:", [heap.extract_min() for _ in range(3)])
    # demonstrate decrease_key
    heap.insert(10); heap.insert(7)
    heap.decrease_key( len(heap.a)-1, 1 )
    print("Min after decrease_key:", heap.find_min())
    print("Delete index 1 (value may vary):", heap.delete(1))
    print("Remaining elements (ascending):", end=" ")
    while True:
        try:
            print(heap.extract_min(), end=" ")
        except IndexError:
            break
    print()

if __name__ == "__main__":
    main()
