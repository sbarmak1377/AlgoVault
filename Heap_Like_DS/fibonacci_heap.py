from __future__ import annotations
from typing import Optional, Iterable

class _FNode:
    __slots__ = ("key", "degree", "parent", "child", "left", "right", "mark")
    def __init__(self, key: int) -> None:
        self.key = key
        self.degree = 0
        self.parent: Optional[_FNode] = None
        self.child: Optional[_FNode] = None
        self.left: _FNode = self
        self.right: _FNode = self
        self.mark = False

def _iterate(root: Optional[_FNode]):
    if not root:
        return
    x = root
    stop = root
    flag = False
    while True:
        if x is stop and flag:
            break
        flag = True
        yield x
        x = x.right

class FibonacciHeap:
    """Min Fibonacci Heap with insert, find_min, extract_min, decrease_key, delete, and merge."""
    def __init__(self, items: Optional[Iterable[int]] = None) -> None:
        self.min: Optional[_FNode] = None
        self.n = 0
        if items:
            for x in items:
                self.insert(x)

    def insert(self, key: int) -> _FNode:
        node = _FNode(key)
        self.min = self._merge_roots(self.min, node)
        self.n += 1
        return node

    @staticmethod
    def _merge_roots(a: Optional[_FNode], b: Optional[_FNode]) -> Optional[_FNode]:
        if not a: return b
        if not b: return a
        # splice b into a's circular list
        a.right.left = b.left
        b.left.right = a.right
        a.right = b
        b.left = a
        return a if a.key <= b.key else b

    def find_min(self) -> int:
        if not self.min:
            raise IndexError("find_min from empty heap")
        return self.min.key

    def merge(self, other: "FibonacciHeap") -> None:
        self.min = self._merge_roots(self.min, other.min)
        self.n += other.n
        other.min = None; other.n = 0

    def extract_min(self) -> int:
        z = self.min
        if not z:
            raise IndexError("extract_min from empty heap")
        # add z's children to root list
        if z.child:
            for x in list(_iterate(z.child)):
                x.parent = None
        self.min = self._remove_from_root_list(z)
        if self.min:
            self._consolidate()
        self.n -= 1
        return z.key

    def _remove_from_root_list(self, z: _FNode) -> Optional[_FNode]:
        if z.right is z:
            root = z.child
        else:
            z.left.right = z.right
            z.right.left = z.left
            root = self.min
        return root

    def _link(self, y: _FNode, x: _FNode) -> None:
        # remove y from roots and make it child of x
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        y.left = y.right = y
        x.child = self._merge_roots(x.child, y)
        x.degree += 1
        y.mark = False

    def _consolidate(self) -> None:
        import math
        A = [None] * (int(math.log2(self.n)) + 3)
        roots = list(_iterate(self.min))
        self.min = None
        for w in roots:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if y.key < x.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        for a in A:
            if a:
                a.left = a.right = a
                self.min = self._merge_roots(self.min, a)

    def decrease_key(self, node_key: int, new_key: int) -> None:
        # find node by key (linear search for simplicity)
        node = self._find(self.min, node_key)
        if not node:
            raise KeyError("key not found")
        if new_key > node.key:
            raise ValueError("new_key greater than current key")
        node.key = new_key
        y = node.parent
        if y and node.key < y.key:
            self._cut(node, y)
            self._cascading_cut(y)
        if self.min and node.key < self.min.key:
            self.min = node

    def _cut(self, x: _FNode, y: _FNode) -> None:
        # remove x from child list of y
        if y.child is x:
            if x.right is x:
                y.child = None
            else:
                y.child = x.right
        x.left.right = x.right
        x.right.left = x.left
        x.left = x.right = x
        y.degree -= 1
        x.parent = None
        self.min = self._merge_roots(self.min, x)
        x.mark = False

    def _cascading_cut(self, y: _FNode) -> None:
        z = y.parent
        if z:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

    def delete(self, node_key: int) -> None:
        self.decrease_key(node_key, float('-inf'))
        self.extract_min()

    def _find(self, root: Optional[_FNode], key: int) -> Optional[_FNode]:
        for x in _iterate(root):
            if x.key == key:
                return x
            res = self._find(x.child, key)
            if res:
                return res
        return None

def main() -> None:
    h = FibonacciHeap([7, 3, 17, 24, 10, 8])
    print("Min:", h.find_min())
    h.insert(1)
    print("After insert 1, min:", h.find_min())
    print("Extract min:", h.extract_min())
    h.decrease_key(24, 2)
    print("Min after decrease_key(24->2):", h.find_min())
    h.delete(10)
    print("Extract remaining in order:", end=" ")
    try:
        while True:
            print(h.extract_min(), end=" ")
    except IndexError:
        pass
    print()

if __name__ == "__main__":
    main()
