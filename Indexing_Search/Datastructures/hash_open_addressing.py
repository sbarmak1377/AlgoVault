from __future__ import annotations
from typing import Any, List, Optional, Iterable

class HashTableOpenAddressing:
    """
    Linear probing open addressing.
    Avg O(1) search/insert/delete at low load; worst O(n).
    """
    _DELETED = object()

    def __init__(self, capacity: int = 16) -> None:
        self._capacity = max(4, capacity)
        self._keys: List[Any] = [None] * self._capacity
        self._vals: List[Any] = [None] * self._capacity
        self._size = 0

    def _idx(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _probe(self, idx: int) -> int:
        return (idx + 1) % self._capacity

    def _resize(self, new_cap: int) -> None:
        old_keys, old_vals = self._keys, self._vals
        self._capacity = new_cap
        self._keys = [None] * self._capacity
        self._vals = [None] * self._capacity
        self._size = 0
        for k, v in zip(old_keys, old_vals):
            if k is not None and k is not self._DELETED:
                self.insert(k, v)

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        if (self._size + 1) / self._capacity > 0.6:
            self._resize(self._capacity * 2)
        i = self._idx(key)
        first_del = None
        while True:
            if self._keys[i] is None:
                insert_at = first_del if first_del is not None else i
                self._keys[insert_at] = key
                self._vals[insert_at] = value
                self._size += 1
                return
            if self._keys[i] is self._DELETED and first_del is None:
                first_del = i
            elif self._keys[i] == key:
                self._vals[i] = value
                return
            i = self._probe(i)

    def search(self, key: Any) -> Optional[Any]:
        i = self._idx(key)
        steps = 0
        while steps < self._capacity:
            if self._keys[i] is None:
                return None
            if self._keys[i] is not self._DELETED and self._keys[i] == key:
                return self._vals[i]
            i = self._probe(i)
            steps += 1
        return None

    def delete(self, key: Any) -> None:
        i = self._idx(key)
        steps = 0
        while steps < self._capacity:
            if self._keys[i] is None:
                return
            if self._keys[i] is not self._DELETED and self._keys[i] == key:
                self._keys[i] = self._DELETED
                self._vals[i] = None
                self._size -= 1
                return
            i = self._probe(i)
            steps += 1

    def build_from(self, items: Iterable[Any]) -> "HashTableOpenAddressing":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    ht = HashTableOpenAddressing().build_from(range(10))
    print("HT(open) search 7:", ht.search(7))
    ht.delete(7); print("HT(open) delete 7, search:", ht.search(7))

if __name__ == "__main__":
    main()
