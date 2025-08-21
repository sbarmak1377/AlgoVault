from __future__ import annotations
from typing import Optional, Iterable

class _Node:
    __slots__ = ("key", "left", "right", "npl")
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Optional[_Node] = None
        self.right: Optional[_Node] = None
        self.npl = 0  # null-path length

def _npl(node: Optional[_Node]) -> int:
    return node.npl if node else -1

class LeftistHeap:
    """Min Leftist Heap with meld, insert, find_min, extract_min, decrease_key (via delete+insert), delete."""
    def __init__(self, items: Optional[Iterable[int]] = None) -> None:
        self.root: Optional[_Node] = None
        if items:
            for x in items:
                self.insert(x)

    def meld(self, other: "LeftistHeap") -> None:
        self.root = self._merge(self.root, other.root)
        other.root = None

    def _merge(self, h1: Optional[_Node], h2: Optional[_Node]) -> Optional[_Node]:
        if not h1: return h2
        if not h2: return h1
        if h1.key > h2.key:
            h1, h2 = h2, h1
        # h1 key <= h2 key
        h1.right = self._merge(h1.right, h2)
        if _npl(h1.left) < _npl(h1.right):
            h1.left, h1.right = h1.right, h1.left
        h1.npl = 1 + max(_npl(h1.left), _npl(h1.right))
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

    def decrease_key(self, key: int, new_key: int) -> None:
        # Simplest implementation: delete then insert
        self.delete(key)
        self.insert(new_key)

    def _delete_node(self, node: Optional[_Node], key: int) -> Optional[_Node]:
        if not node:
            return None
        if node.key == key:
            return self._merge(node.left, node.right)
        node.left = self._delete_node(node.left, key)
        node.right = self._delete_node(node.right, key)
        if _npl(node.left) < _npl(node.right):
            node.left, node.right = node.right, node.left
        node.npl = 1 + max(_npl(node.left), _npl(node.right))
        return node

    def delete(self, key: int) -> None:
        self.root = self._delete_node(self.root, key)

def main() -> None:
    h = LeftistHeap([10, 3, 7, 1, 14])
    print("Min:", h.find_min())
    h.insert(0)
    print("After insert 0, min:", h.find_min())
    print("Extract min:", h.extract_min())
    h.decrease_key(10, 2)
    print("Min after decrease_key(10->2):", h.find_min())
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
