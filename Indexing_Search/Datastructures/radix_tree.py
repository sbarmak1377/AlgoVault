from __future__ import annotations
from typing import Any, Dict, Optional, Iterable, List, Tuple

class RadixNode:
    def __init__(self) -> None:
        self.children: Dict[str, RadixNode] = {}
        self.value: Optional[Any] = None
        self.terminal: bool = False

class RadixTree:
    """
    Radix (compressed) trie.
    ~O(L) on substring comparisons.
    """
    def __init__(self) -> None:
        self._root = RadixNode()

    def _split_edge(self, parent: RadixNode, edge: str, split_idx: int) -> None:
        child = parent.children.pop(edge)
        mid = RadixNode()
        parent.children[edge[:split_idx]] = mid
        mid.children[edge[split_idx:]] = child

    def insert(self, key: str, value: Any = None) -> None:
        value = key if value is None else value
        node = self._root
        k = key
        while True:
            for edge, child in list(node.children.items()):
                i = 0
                while i < len(edge) and i < len(k) and edge[i] == k[i]:
                    i += 1
                if i == 0:
                    continue
                if i < len(edge):
                    self._split_edge(node, edge, i)
                    node = node.children[edge[:i]]
                else:
                    node = child
                k = k[i:]
                if not k:
                    node.terminal = True
                    node.value = value
                    return
                break
            else:
                node.children[k] = RadixNode()
                node = node.children[k]
                node.terminal = True
                node.value = value
                return

    def search(self, key: str):
        node = self._root
        k = key
        while k:
            matched = False
            for edge, child in node.children.items():
                if k.startswith(edge):
                    k = k[len(edge):]
                    node = child
                    matched = True
                    break
            if not matched:
                return None
        return node.value if node.terminal else None

    def delete(self, key: str) -> None:
        stack: List[Tuple[RadixNode, str]] = []
        node = self._root
        k = key
        while k:
            for edge, child in node.children.items():
                if k.startswith(edge):
                    stack.append((node, edge))
                    node = child
                    k = k[len(edge):]
                    break
            else:
                return
        if not node.terminal:
            return
        node.terminal = False
        node.value = None
        while stack:
            parent, edge = stack.pop()
            child = parent.children[edge]
            if not child.terminal and not child.children:
                del parent.children[edge]
            elif not child.terminal and len(child.children) == 1:
                (g_edge, g_child), = child.children.items()
                del parent.children[edge]
                parent.children[edge + g_edge] = g_child
            else:
                break

    def build_from(self, items: Iterable[str]) -> "RadixTree":
        for x in items:
            self.insert(str(x))
        return self

def main() -> None:
    rt = RadixTree().build_from(["bear", "bell", "bid", "bull", "buy", "sell", "stock", "stop"])
    print("Radix search 'bull':", rt.search("bull"))
    rt.delete("bull"); print("Radix delete 'bull', search:", rt.search("bull"))

if __name__ == "__main__":
    main()
