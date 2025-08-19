from __future__ import annotations
from typing import Any, List, Tuple, Optional, Iterable

class HashTableChaining:
    """
    Separate chaining hash table.
    Avg O(1) search/insert/delete; worst O(n).
    """
    def __init__(self, capacity: int = 16) -> None:
        self._buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(max(4, capacity))]
        self._size = 0

    def _bucket_index(self, key: Any) -> int:
        return hash(key) % len(self._buckets)

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / len(self._buckets) > 0.75:
            self._resize(len(self._buckets) * 2)

    def _resize(self, new_cap: int) -> None:
        old = self._buckets
        self._buckets = [[] for _ in range(new_cap)]
        self._size = 0
        for bucket in old:
            for k, v in bucket:
                self.insert(k, v)

    def search(self, key: Any) -> Optional[Any]:
        idx = self._bucket_index(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> None:
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return

    def build_from(self, items: Iterable[Any]) -> "HashTableChaining":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    ht = HashTableChaining().build_from(["a", "b", "c", "x"])
    print("HT(chain) search 'b':", ht.search("b"))
    ht.delete("b"); print("HT(chain) delete 'b', search:", ht.search("b"))

if __name__ == "__main__":
    main()
