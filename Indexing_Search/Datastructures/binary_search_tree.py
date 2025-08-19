from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Iterable

@dataclass
class _BSTNode:
    key: Any
    value: Any
    left: Optional["_BSTNode"] = None
    right: Optional["_BSTNode"] = None

class BinarySearchTree:
    """
    Unbalanced Binary Search Tree.
    Logic: insert/search by key order (left < key < right).
    Time: average O(log n); worst O(n). Space: O(n).
    """
    def __init__(self) -> None:
        self._root: Optional[_BSTNode] = None

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        self._root = self._insert(self._root, key, value)

    def _insert(self, node: Optional[_BSTNode], key: Any, value: Any) -> _BSTNode:
        if node is None:
            return _BSTNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
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

    def delete(self, key: Any) -> None:
        self._root = self._delete(self._root, key)

    def _min_node(self, node: _BSTNode) -> _BSTNode:
        while node.left:
            node = node.left
        return node

    def _delete(self, node: Optional[_BSTNode], key: Any) -> Optional[_BSTNode]:
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
        return node

    def build_from(self, items: Iterable[Any]) -> "BinarySearchTree":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    bst = BinarySearchTree().build_from([7, 3, 9, 1, 5])
    print("BST search 5:", bst.search(5))
    print("BST search 3:", bst.search(3))
    bst.delete(3); print("BST delete 3, search 3:", bst.search(3))
    bst.delete(7); print("BST delete 7(root), search 7:", bst.search(7))

if __name__ == "__main__":
    main()
