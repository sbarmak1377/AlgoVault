from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Iterable

RED = True
BLACK = False

@dataclass
class _RBNode:
    key: Any
    value: Any
    color: bool = RED
    left: Optional["_RBNode"] = None
    right: Optional["_RBNode"] = None

class RedBlackTree:
    """
    Left-leaning Red-Black Tree (LLRB) with insert/search/delete.
    Time: amortized O(log n). Space: O(n).
    """
    def __init__(self) -> None:
        self._root: Optional[_RBNode] = None

    def _is_red(self, n: Optional[_RBNode]) -> bool:
        return bool(n and n.color == RED)

    def _rotate_left(self, h: _RBNode) -> _RBNode:
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def _rotate_right(self, h: _RBNode) -> _RBNode:
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def _flip_colors(self, h: _RBNode) -> None:
        h.color = not h.color
        if h.left:  h.left.color = not h.left.color
        if h.right: h.right.color = not h.right.color

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        self._root = self._insert(self._root, key, value)
        self._root.color = BLACK

    def _insert(self, h: Optional[_RBNode], key: Any, value: Any) -> _RBNode:
        if h is None:
            return _RBNode(key, value, RED)
        if key < h.key:
            h.left = self._insert(h.left, key, value)
        elif key > h.key:
            h.right = self._insert(h.right, key, value)
        else:
            h.value = value

        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)
        return h

    def search(self, key: Any) -> Optional[Any]:
        x = self._root
        while x:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x.value
        return None

    # ---------- Deletion (LLRB top-down) ----------
    def _move_red_left(self, h: _RBNode) -> _RBNode:
        self._flip_colors(h)
        if self._is_red(h.right.left):
            h.right = self._rotate_right(h.right)
            h = self._rotate_left(h)
            self._flip_colors(h)
        return h

    def _move_red_right(self, h: _RBNode) -> _RBNode:
        self._flip_colors(h)
        if self._is_red(h.left.left):
            h = self._rotate_right(h)
            self._flip_colors(h)
        return h

    def _fix_up(self, h: _RBNode) -> _RBNode:
        if self._is_red(h.right):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)
        return h

    def _min_node(self, h: _RBNode) -> _RBNode:
        while h.left:
            h = h.left
        return h

    def _delete_min(self, h: _RBNode) -> Optional[_RBNode]:
        if h.left is None:
            return None
        if not self._is_red(h.left) and not self._is_red(h.left.left):
            h = self._move_red_left(h)
        h.left = self._delete_min(h.left)
        return self._fix_up(h)

    def delete_min(self) -> None:
        if self._root is None:
            return
        if not self._is_red(self._root.left) and not self._is_red(self._root.right):
            self._root.color = RED
        self._root = self._delete_min(self._root)
        if self._root:
            self._root.color = BLACK

    def delete(self, key: Any) -> None:
        if self._root is None:
            return
        # Optional: fast path if not found
        x = self.search(key)
        if x is None:
            return
        if not self._is_red(self._root.left) and not self._is_red(self._root.right):
            self._root.color = RED
        self._root = self._delete(self._root, key)
        if self._root:
            self._root.color = BLACK

    def _delete(self, h: _RBNode, key: Any) -> Optional[_RBNode]:
        if key < h.key:
            if h.left:
                if not self._is_red(h.left) and not self._is_red(h.left.left):
                    h = self._move_red_left(h)
                h.left = self._delete(h.left, key)
        else:
            if self._is_red(h.left):
                h = self._rotate_right(h)
            if key == h.key and (h.right is None):
                return None
            if h.right and (not self._is_red(h.right) and not self._is_red(h.right.left)):
                h = self._move_red_right(h)
            if key == h.key:
                m = self._min_node(h.right)
                h.key, h.value = m.key, m.value
                h.right = self._delete_min(h.right)
            else:
                h.right = self._delete(h.right, key)
        return self._fix_up(h)

    def build_from(self, items: Iterable[Any]) -> "RedBlackTree":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    rbt = RedBlackTree().build_from([10, 20, 30, 15, 25, 5, 1, 50, 60, 55])
    print("RBT search 25:", rbt.search(25))
    rbt.delete(20); print("RBT delete 20, search 20:", rbt.search(20))
    rbt.delete(10); print("RBT delete 10, search 10:", rbt.search(10))
    rbt.delete(55); print("RBT delete 55, search 55:", rbt.search(55))

if __name__ == "__main__":
    main()
