from __future__ import annotations
from typing import Optional, Iterable, Tuple

class _Node:
    __slots__ = ("key", "degree", "parent", "child", "sibling")
    def __init__(self, key: int) -> None:
        self.key = key
        self.degree = 0
        self.parent: Optional[_Node] = None
        self.child: Optional[_Node] = None
        self.sibling: Optional[_Node] = None

class BinomialHeap:
    """Min Binomial Heap supporting insert, find_min, extract_min, decrease_key, delete, and meld."""
    def __init__(self, items: Optional[Iterable[int]] = None) -> None:
        self.head: Optional[_Node] = None
        if items:
            for x in items:
                self.insert(x)

    # Merge root lists by degree (like merging two binary numbers)
    @staticmethod
    def _merge(h1: Optional[_Node], h2: Optional[_Node]) -> Optional[_Node]:
        if not h1: return h2
        if not h2: return h1
        if h1.degree <= h2.degree:
            head = h1; h1 = h1.sibling
        else:
            head = h2; h2 = h2.sibling
        tail = head
        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling = h1; h1 = h1.sibling
            else:
                tail.sibling = h2; h2 = h2.sibling
            tail = tail.sibling
        tail.sibling = h1 if h1 else h2
        return head

    @staticmethod
    def _link(y: _Node, z: _Node) -> None:
        # make y a child of z; assumes y.key >= z.key and y.degree == z.degree
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def meld(self, other: "BinomialHeap") -> None:
        self.head = self._union(self.head, other.head)
        other.head = None

    def _union(self, h1: Optional[_Node], h2: Optional[_Node]) -> Optional[_Node]:
        new_head = self._merge(h1, h2)
        if not new_head:
            return None
        prev = None
        curr = new_head
        next = curr.sibling
        while next:
            if curr.degree != next.degree or (next.sibling and next.sibling.degree == curr.degree):
                prev = curr
                curr = next
            elif curr.key <= next.key:
                curr.sibling = next.sibling
                self._link(next, curr)
            else:
                if prev:
                    prev.sibling = next
                else:
                    new_head = next
                self._link(curr, next)
                curr = next
            next = curr.sibling
        return new_head

    def insert(self, key: int) -> None:
        temp = BinomialHeap([key])
        self.head = self._union(self.head, temp.head)
        temp.head = None

    def find_min(self) -> int:
        if not self.head:
            raise IndexError("find_min from empty heap")
        y = None
        x = self.head
        m = float('inf')
        while x:
            if x.key < m:
                m = x.key; y = x
            x = x.sibling
        return y.key  # type: ignore

    def _extract_min_node(self) -> _Node:
        if not self.head:
            raise IndexError("extract_min from empty heap")
        prev_min = None
        min_node = self.head
        prev = None
        curr = self.head
        while curr:
            if curr.key < min_node.key:
                min_node = curr; prev_min = prev
            prev = curr; curr = curr.sibling
        if prev_min:
            prev_min.sibling = min_node.sibling
        else:
            self.head = min_node.sibling
        # reverse min_node's children into a new heap list
        child = min_node.child
        prev = None
        while child:
            nxt = child.sibling
            child.sibling = prev
            child.parent = None
            prev = child
            child = nxt
        self.head = self._union(self.head, prev)
        return min_node

    def extract_min(self) -> int:
        node = self._extract_min_node()
        return node.key

    def _find_node(self, node: Optional[_Node], key: int) -> Optional[_Node]:
        while node:
            if node.key == key:
                return node
            res = self._find_node(node.child, key)
            if res:
                return res
            node = node.sibling
        return None

    def decrease_key(self, key: int, new_key: int) -> None:
        node = self._find_node(self.head, key)
        if not node:
            raise KeyError("key not found")
        if new_key > node.key:
            raise ValueError("new_key must be <= current key")
        node.key = new_key
        y = node
        z = y.parent
        while z and y.key < z.key:
            y.key, z.key = z.key, y.key
            y = z
            z = y.parent

    def delete(self, key: int) -> None:
        self.decrease_key(key, float('-inf'))
        self.extract_min()

def main() -> None:
    h = BinomialHeap([10, 3, 7, 1, 14])
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
