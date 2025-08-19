from __future__ import annotations
from typing import Any, List, Optional, Iterable, Tuple, Union

class BPlusLeaf:
    def __init__(self) -> None:
        self.keys: List[Any] = []
        self.values: List[Any] = []
        self.next: Optional["BPlusLeaf"] = None

class BPlusInternal:
    def __init__(self) -> None:
        self.keys: List[Any] = []
        self.children: List[Union["BPlusInternal", BPlusLeaf]] = []

Node = Union[BPlusInternal, BPlusLeaf]

class BPlusTree:
    """
    Simplified B+ Tree with insert/search/delete.
    Values in leaves; internal nodes hold separators; leaves are linked.
    """
    def __init__(self, order: int = 4) -> None:
        if order < 3:
            raise ValueError("B+Tree order must be >= 3")
        self.order = order
        self.root: Node = BPlusLeaf()

    def search(self, key: Any):
        node = self.root
        while isinstance(node, BPlusInternal):
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        for i, k in enumerate(node.keys):
            if k == key:
                return node.values[i]
        return None

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        root = self.root
        split_key, right = self._insert_recursive(root, key, value)
        if split_key is not None:
            new_root = BPlusInternal()
            new_root.keys = [split_key]
            new_root.children = [root, right]
            self.root = new_root

    def _insert_recursive(self, node: Node, key: Any, value: Any):
        if isinstance(node, BPlusLeaf):
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i] = value
                return None, None
            node.keys.insert(i, key)
            node.values.insert(i, value)
            if len(node.keys) > self.order:
                return self._split_leaf(node)
            return None, None
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            split_key, right_child = self._insert_recursive(node.children[i], key, value)
            if split_key is None:
                return None, None
            node.keys.insert(i, split_key)
            node.children.insert(i+1, right_child)
            if len(node.keys) > self.order:
                return self._split_internal(node)
            return None, None

    def _split_leaf(self, leaf: BPlusLeaf):
        mid = (len(leaf.keys) + 1) // 2
        right = BPlusLeaf()
        right.keys = leaf.keys[mid:]
        right.values = leaf.values[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        right.next = leaf.next
        leaf.next = right
        return right.keys[0], right

    def _split_internal(self, node: BPlusInternal):
        mid = len(node.keys) // 2
        split_key = node.keys[mid]
        right = BPlusInternal()
        right.keys = node.keys[mid+1:]
        right.children = node.children[mid+1:]
        node.keys = node.keys[:mid]
        node.children = node.children[:mid+1]
        return split_key, right

    # -------- Delete --------
    def delete(self, key: Any) -> None:
        if isinstance(self.root, BPlusLeaf):
            self._leaf_delete(self.root, key)
            return
        self._delete_recursive(None, self.root, key, child_index=None)
        if isinstance(self.root, BPlusInternal) and len(self.root.keys) == 0:
            self.root = self.root.children[0]

    def _delete_recursive(self, parent: Optional[BPlusInternal], node: Node, key: Any, child_index: Optional[int]):
        if isinstance(node, BPlusLeaf):
            changed = self._leaf_delete(node, key)
            if changed and parent is not None:
                self._rebalance_after_delete(parent, child_index)
            return
        i = 0
        while i < len(node.keys) and key >= node.keys[i]:
            i += 1
        self._delete_recursive(node, node.children[i], key, i)
        self._rebalance_after_delete(node, i)

    def _leaf_delete(self, leaf: BPlusLeaf, key: Any) -> bool:
        try:
            idx = leaf.keys.index(key)
        except ValueError:
            return False
        leaf.keys.pop(idx); leaf.values.pop(idx)
        return True

    def _rebalance_after_delete(self, parent: BPlusInternal, i: int) -> None:
        child = parent.children[i]
        min_keys = (self.order + 1)//2
        if isinstance(child, BPlusLeaf):
            if len(child.keys) >= max(1, min_keys-1):
                return
        else:
            if len(child.keys) >= max(1, min_keys-1):
                return

        if i > 0:
            left = parent.children[i-1]
            if isinstance(child, BPlusLeaf) and len(left.keys) > min_keys-1:
                child.keys.insert(0, left.keys.pop())
                child.values.insert(0, left.values.pop())
                parent.keys[i-1] = child.keys[0]
                return
            if isinstance(child, BPlusInternal) and len(left.keys) >= min_keys:
                child.children.insert(0, left.children.pop())
                child.keys.insert(0, parent.keys[i-1])
                parent.keys[i-1] = left.keys.pop()
                return
        if i < len(parent.children)-1:
            right = parent.children[i+1]
            if isinstance(child, BPlusLeaf) and len(right.keys) > min_keys-1:
                child.keys.append(right.keys.pop(0))
                child.values.append(right.values.pop(0))
                parent.keys[i] = right.keys[0]
                return
            if isinstance(child, BPlusInternal) and len(right.keys) >= min_keys:
                child.children.append(right.children.pop(0))
                child.keys.append(parent.keys[i])
                parent.keys[i] = right.keys.pop(0)
                return

        if i > 0:
            left = parent.children[i-1]
            self._merge_nodes(parent, i-1, left, child)
        else:
            right = parent.children[i+1]
            self._merge_nodes(parent, i, child, right)

    def _merge_nodes(self, parent: BPlusInternal, idx: int, left: Node, right: Node) -> None:
        if isinstance(left, BPlusLeaf) and isinstance(right, BPlusLeaf):
            left.keys.extend(right.keys); left.values.extend(right.values)
            left.next = right.next
            parent.keys.pop(idx); parent.children.pop(idx+1)
        elif isinstance(left, BPlusInternal) and isinstance(right, BPlusInternal):
            sep = parent.keys.pop(idx)
            left.keys.append(sep)
            left.keys.extend(right.keys)
            left.children.extend(right.children)
            parent.children.pop(idx+1)

    def build_from(self, items: Iterable[Any]) -> "BPlusTree":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    bpt = BPlusTree(order=3).build_from([10,20,5,6,12,30,7,17])
    print("B+ search 12:", bpt.search(12))
    bpt.delete(12); print("B+ delete 12, search:", bpt.search(12))
    bpt.delete(5); print("B+ delete 5, search:", bpt.search(5))

if __name__ == "__main__":
    main()
