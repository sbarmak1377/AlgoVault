from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Iterable

@dataclass
class _SplayNode:
    key: Any
    value: Any
    left: Optional["_SplayNode"] = None
    right: Optional["_SplayNode"] = None

class SplayTree:
    """
    Splay tree (self-adjusting). Amortized O(log n); worst O(n).
    """
    def __init__(self) -> None:
        self._root: Optional[_SplayNode] = None

    def _rotate_right(self, x: _SplayNode) -> _SplayNode:
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _rotate_left(self, x: _SplayNode) -> _SplayNode:
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root: Optional[_SplayNode], key: Any) -> Optional[_SplayNode]:
        if root is None or root.key == key:
            return root
        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return root if root.left is None else self._rotate_right(root)
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            return root if root.right is None else self._rotate_left(root)

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        if self._root is None:
            self._root = _SplayNode(key, value)
            return
        self._root = self._splay(self._root, key)
        if key == self._root.key:
            self._root.value = value
            return
        new_node = _SplayNode(key, value)
        if key < self._root.key:
            new_node.right = self._root
            new_node.left = self._root.left
            self._root.left = None
        else:
            new_node.left = self._root
            new_node.right = self._root.right
            self._root.right = None
        self._root = new_node

    def search(self, key: Any) -> Optional[Any]:
        self._root = self._splay(self._root, key)
        if self._root and self._root.key == key:
            return self._root.value
        return None

    def delete(self, key: Any) -> None:
        if self._root is None:
            return
        self._root = self._splay(self._root, key)
        if self._root.key != key:
            return
        left = self._root.left
        right = self._root.right
        self._root = None
        if left is None:
            self._root = right
        else:
            x = left
            while x.right:
                x = x.right
            left = self._splay(left, x.key)
            left.right = right
            self._root = left

    def build_from(self, items: Iterable[Any]) -> "SplayTree":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    st = SplayTree().build_from([10, 20, 30, 40, 50])
    print("Splay search 30:", st.search(30))
    st.delete(30); print("Splay delete 30, search 30:", st.search(30))
    st.delete(10); print("Splay delete 10, search 10:", st.search(10))

if __name__ == "__main__":
    main()
