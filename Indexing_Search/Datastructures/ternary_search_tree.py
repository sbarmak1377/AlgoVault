from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Iterable

@dataclass
class _TSTNode:
    ch: str
    left: Optional["_TSTNode"] = None
    eq: Optional["_TSTNode"] = None
    right: Optional["_TSTNode"] = None
    value: Optional[Any] = None
    terminal: bool = False

class TernarySearchTree:
    """
    TST with insert/search/delete.
    """
    def __init__(self) -> None:
        self._root: Optional[_TSTNode] = None

    def insert(self, key: str, value: Any = None) -> None:
        value = key if value is None else value
        if not key:
            return
        self._root = self._insert(self._root, key, 0, value)

    def _insert(self, node: Optional[_TSTNode], key: str, i: int, value: Any) -> _TSTNode:
        ch = key[i]
        if node is None:
            node = _TSTNode(ch)
        if ch < node.ch:
            node.left = self._insert(node.left, key, i, value)
        elif ch > node.ch:
            node.right = self._insert(node.right, key, i, value)
        else:
            if i + 1 == len(key):
                node.terminal = True
                node.value = value
            else:
                node.eq = self._insert(node.eq, key, i + 1, value)
        return node

    def search(self, key: str):
        node = self._root
        i = 0
        while node and i < len(key):
            ch = key[i]
            if ch < node.ch:
                node = node.left
            elif ch > node.ch:
                node = node.right
            else:
                i += 1
                if i == len(key):
                    return node.value if node.terminal else None
                node = node.eq
        return None

    def delete(self, key: str) -> None:
        def _delete(node: Optional[_TSTNode], i: int) -> Optional[_TSTNode]:
            if node is None:
                return None
            ch = key[i]
            if ch < node.ch:
                node.left = _delete(node.left, i)
            elif ch > node.ch:
                node.right = _delete(node.right, i)
            else:
                if i + 1 == len(key):
                    node.terminal = False
                    node.value = None
                else:
                    node.eq = _delete(node.eq, i + 1)
                if not node.terminal and node.eq is None:
                    if node.left is None: return node.right
                    if node.right is None: return node.left
            return node
        if key:
            self._root = _delete(self._root, 0)

    def build_from(self, items: Iterable[str]) -> "TernarySearchTree":
        for x in items:
            s = str(x)
            if s:
                self.insert(s)
        return self

def main() -> None:
    tst = TernarySearchTree().build_from(["cat", "cap", "cup", "dog"])
    print("TST search 'cap':", tst.search("cap"))
    tst.delete("cap"); print("TST delete 'cap', search:", tst.search("cap"))

if __name__ == "__main__":
    main()
