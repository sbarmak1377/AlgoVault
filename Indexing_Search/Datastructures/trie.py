from __future__ import annotations
from typing import Any, Dict, Optional, Iterable

class TrieNode:
    __slots__ = ("children", "value", "terminal")
    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.value: Optional[Any] = None
        self.terminal: bool = False

class Trie:
    """
    Trie (prefix tree) for strings.
    insert/search/delete O(L), L = key length.
    """
    def __init__(self) -> None:
        self._root = TrieNode()

    def insert(self, key: str, value: Any = None) -> None:
        value = key if value is None else value
        node = self._root
        for ch in key:
            node = node.children.setdefault(ch, TrieNode())
        node.terminal = True
        node.value = value

    def search(self, key: str):
        node = self._root
        for ch in key:
            node = node.children.get(ch)
            if node is None:
                return None
        return node.value if node.terminal else None

    def delete(self, key: str) -> None:
        def _delete(node: TrieNode, idx: int) -> bool:
            if idx == len(key):
                if not node.terminal:
                    return False
                node.terminal = False
                node.value = None
                return len(node.children) == 0
            ch = key[idx]
            child = node.children.get(ch)
            if child is None:
                return False
            should_prune = _delete(child, idx + 1)
            if should_prune:
                del node.children[ch]
            return not node.terminal and len(node.children) == 0
        _delete(self._root, 0)

    def build_from(self, items: Iterable[str]) -> "Trie":
        for x in items:
            self.insert(str(x))
        return self

def main() -> None:
    trie = Trie().build_from(["cat", "car", "dog", "hamster", "lion", "hackathon"])
    print("Trie search 'car':", trie.search("car"))
    print("Trie search 'ha':", trie.search("ha"))
    print("Trie search 'l':", trie.search("l"))
    trie.delete("car"); print("Trie delete 'car', search:", trie.search("car"))

if __name__ == "__main__":
    main()
