from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Iterable

@dataclass
class _AVLNode:
    key: Any
    value: Any
    left: Optional["_AVLNode"] = None
    right: Optional["_AVLNode"] = None
    height: int = 1

class AVLTree:
    """
    AVL Tree (height-balanced BST: |balance_factor| <= 1).
    Time: search/insert/delete O(log n). Space: O(n).
    """
    def __init__(self) -> None:
        self._root: Optional[_AVLNode] = None

    def _height(self, n: Optional[_AVLNode]) -> int:
        return n.height if n else 0

    def _balance(self, n: Optional[_AVLNode]) -> int:
        return (self._height(n.left) - self._height(n.right)) if n else 0

    def _fix_height(self, n: _AVLNode) -> None:
        n.height = 1 + max(self._height(n.left), self._height(n.right))

    def _rotate_right(self, y: _AVLNode) -> _AVLNode:
        x = y.left
        T2 = x.right if x else None
        x.right = y
        y.left = T2
        self._fix_height(y)
        self._fix_height(x)
        return x

    def _rotate_left(self, x: _AVLNode) -> _AVLNode:
        y = x.right
        T2 = y.left if y else None
        y.left = x
        x.right = T2
        self._fix_height(x)
        self._fix_height(y)
        return y

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        self._root = self._insert(self._root, key, value)

    def _insert(self, node: Optional[_AVLNode], key: Any, value: Any) -> _AVLNode:
        if node is None:
            return _AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node

        self._fix_height(node)
        bf = self._balance(node)
        if bf > 1 and key < node.left.key:        # LL
            return self._rotate_right(node)
        if bf < -1 and key > node.right.key:      # RR
            return self._rotate_left(node)
        if bf > 1 and key > node.left.key:        # LR
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bf < -1 and key < node.right.key:      # RL
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _min_node(self, node: _AVLNode) -> _AVLNode:
        while node.left:
            node = node.left
        return node

    def delete(self, key: Any) -> None:
        self._root = self._delete(self._root, key)

    def _delete(self, node: Optional[_AVLNode], key: Any) -> Optional[_AVLNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None: return node.right
            if node.right is None: return node.left
            succ = self._min_node(node.right)
            node.key, node.value = succ.key, succ.value
            node.right = self._delete(node.right, succ.key)

        self._fix_height(node)
        bf = self._balance(node)
        if bf > 1:
            if self._balance(node.left) < 0:   # LR
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)    # LL
        if bf < -1:
            if self._balance(node.right) > 0:  # RL
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)     # RR
        return node

    def search(self, key: Any) -> Optional[Any]:
        node = self._root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return None

    def build_from(self, items: Iterable[Any]) -> "AVLTree":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    avl = AVLTree().build_from([10, 20, 30, 40, 50, 25])
    print("AVL search 25:", avl.search(25))
    avl.delete(30); print("AVL delete 30, search 30:", avl.search(30))
    avl.delete(10); print("AVL delete 10, search 10:", avl.search(10))

if __name__ == "__main__":
    main()
