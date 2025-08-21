from __future__ import annotations
from typing import Optional, Iterable

class _Node:
    __slots__ = ("key", "left", "right")
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Optional[_Node] = None
        self.right: Optional[_Node] = None

class SkewHeap:
    """Min Skew Heap: mergeable, self-adjusting heap. Supports insert, find_min, extract_min, meld."""
    def __init__(self, items: Optional[Iterable[int]] = None) -> None:
        self.root: Optional[_Node] = None
        if items:
            for x in items:
                self.insert(x)

    def meld(self, other: "SkewHeap") -> None:
        self.root = self._merge(self.root, other.root)
        other.root = None

    def _merge(self, h1: Optional[_Node], h2: Optional[_Node]) -> Optional[_Node]:
        if not h1: return h2
        if not h2: return h1
        if h1.key > h2.key:
            h1, h2 = h2, h1
        # swap children and merge with former left child
        h1.left, h1.right = h1.right, h1.left
        h1.left = self._merge(h2, h1.left)
        return h1

    def insert(self, key: int) -> None:
        node = _Node(key)
        self.root = self._merge(self.root, node)

    def find_min(self) -> int:
        if not self.root:
            raise IndexError("find_min from empty heap")
        return self.root.key

    def extract_min(self) -> int:
        if not self.root:
            raise IndexError("extract_min from empty heap")
        m = self.root.key
        self.root = self._merge(self.root.left, self.root.right)
        return m

    # decrease_key/delete not naturally supported; emulate via rebuild:
    def decrease_key(self, key: int, new_key: int) -> None:
        self.delete(key)
        self.insert(new_key)

    def _delete_node(self, node: Optional[_Node], key: int) -> Optional[_Node]:
        if not node:
            return None
        if node.key == key:
            return self._merge(node.left, node.right)
        node.left = self._delete_node(node.left, key)
        node.right = self._delete_node(node.right, key)
        return node

    def delete(self, key: int) -> None:
        self.root = self._delete_node(self.root, key)

def main() -> None:
    h = SkewHeap([5, 9, 3, 7, 2])
    print("Min:", h.find_min())
    h.insert(1)
    print("After insert 1, min:", h.find_min())
    print("Extract min:", h.extract_min())
    h.decrease_key(9, 0)
    print("Min after decrease_key(9->0):", h.find_min())
    h.delete(7)
    print("Extract remaining in order:", end=" ")
    try:
        while True:
            print(h.extract_min(), end=" ")
    except IndexError:
        pass
    print()

if __name__ == "__main__":
    main()
