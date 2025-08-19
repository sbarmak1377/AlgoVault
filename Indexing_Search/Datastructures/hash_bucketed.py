from __future__ import annotations
from typing import Any, List, Optional, Iterable

class HashTableBucketed:
    """
    Bucketed open addressing: k slots per bucket.
    Avg O(1) until buckets overflow.
    """
    def __init__(self, capacity: int = 16, bucket_size: int = 4) -> None:
        self._capacity = max(4, capacity)
        self._bucket_size = max(2, bucket_size)
        self._keys: List[List[Any]] = [[None]*self._bucket_size for _ in range(self._capacity)]
        self._vals: List[List[Any]] = [[None]*self._bucket_size for _ in range(self._capacity)]
        self._size = 0

    def _idx(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self, new_cap: int) -> None:
        old = [(k, v) for rowk, rowv in zip(self._keys, self._vals) for k, v in zip(rowk, rowv) if k is not None]
        self._capacity = new_cap
        self._keys = [[None]*self._bucket_size for _ in range(self._capacity)]
        self._vals = [[None]*self._bucket_size for _ in range(self._capacity)]
        self._size = 0
        for k, v in old:
            self.insert(k, v)

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        if (self._size + 1) / (self._capacity * self._bucket_size) > 0.7:
            self._resize(self._capacity * 2)
        i = self._idx(key)
        for j in range(self._bucket_size):
            if self._keys[i][j] is None or self._keys[i][j] == key:
                if self._keys[i][j] is None:
                    self._size += 1
                self._keys[i][j] = key
                self._vals[i][j] = value
                return
        start = i
        i = (i + 1) % self._capacity
        while i != start:
            for j in range(self._bucket_size):
                if self._keys[i][j] is None:
                    self._keys[i][j] = key
                    self._vals[i][j] = value
                    self._size += 1
                    return
            i = (i + 1) % self._capacity
        raise RuntimeError("HashTableBucketed is full")

    def search(self, key: Any):
        i = self._idx(key)
        for j in range(self._bucket_size):
            if self._keys[i][j] == key:
                return self._vals[i][j]
        start = i
        i = (i + 1) % self._capacity
        while i != start:
            for j in range(self._bucket_size):
                if self._keys[i][j] == key:
                    return self._vals[i][j]
            i = (i + 1) % self._capacity
        return None

    def delete(self, key: Any) -> None:
        i = self._idx(key)
        for j in range(self._bucket_size):
            if self._keys[i][j] == key:
                self._keys[i][j] = None
                self._vals[i][j] = None
                self._size -= 1
                return
        start = i
        i = (i + 1) % self._capacity
        while i != start:
            for j in range(self._bucket_size):
                if self._keys[i][j] == key:
                    self._keys[i][j] = None
                    self._vals[i][j] = None
                    self._size -= 1
                    return
            i = (i + 1) % self._capacity

    def build_from(self, items: Iterable[Any]) -> "HashTableBucketed":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    hb = HashTableBucketed().build_from([1,2,3,4,5,6,7,8,9])
    print("HT(bucket) search 6:", hb.search(6))
    hb.delete(6); print("HT(bucket) delete 6, search:", hb.search(6))

if __name__ == "__main__":
    main()
