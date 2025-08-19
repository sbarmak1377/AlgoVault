from __future__ import annotations
from typing import Any, List, Optional, Iterable

class BTreeNode:
    def __init__(self, t: int, leaf: bool) -> None:
        self.t = t
        self.leaf = leaf
        self.keys: List[Any] = []
        self.children: List["BTreeNode"] = []
        self.values: List[Any] = []  # parallel to keys

class BTree:
    """
    B-Tree (min degree t >= 2) with insert/search/delete.
    """
    def __init__(self, t: int = 3) -> None:
        if t < 2:
            raise ValueError("B-Tree minimum degree t must be >= 2")
        self.t = t
        self.root = BTreeNode(t, True)

    def search(self, key: Any):
        return self._search(self.root, key)

    def _search(self, node: BTreeNode, key: Any):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        if node.leaf:
            return None
        return self._search(node.children[i], key)

    def insert(self, key: Any, value: Any = None) -> None:
        value = key if value is None else value
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, False)
            s.children.append(r)
            self.root = s
            self._split_child(s, 0)
            self._insert_nonfull(s, key, value)
        else:
            self._insert_nonfull(r, key, value)

    def _split_child(self, parent: BTreeNode, i: int) -> None:
        t = self.t
        y = parent.children[i]
        z = BTreeNode(t, y.leaf)
        parent.keys.insert(i, y.keys[t-1])
        parent.values.insert(i, y.values[t-1])
        parent.children.insert(i+1, z)
        z.keys = y.keys[t:]
        z.values = y.values[t:]
        y.keys = y.keys[:t-1]
        y.values = y.values[:t-1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

    def _insert_nonfull(self, node: BTreeNode, key: Any, value: Any) -> None:
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
            node.keys[i+1] = key
            node.values[i+1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2*self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key, value)

    def delete(self, key: Any) -> None:
        self._delete(self.root, key)
        if not self.root.leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]

    def _delete(self, node: BTreeNode, key: Any) -> None:
        t = self.t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                node.keys.pop(i); node.values.pop(i)
            else:
                if len(node.children[i].keys) >= t:
                    pred_node = node.children[i]
                    while not pred_node.leaf:
                        pred_node = pred_node.children[-1]
                    node.keys[i] = pred_node.keys[-1]
                    node.values[i] = pred_node.values[-1]
                    self._delete(node.children[i], node.keys[i])
                elif len(node.children[i+1].keys) >= t:
                    succ_node = node.children[i+1]
                    while not succ_node.leaf:
                        succ_node = succ_node.children[0]
                    node.keys[i] = succ_node.keys[0]
                    node.values[i] = succ_node.values[0]
                    self._delete(node.children[i+1], node.keys[i])
                else:
                    self._merge(node, i)
                    self._delete(node.children[i], key)
        else:
            if node.leaf:
                return
            if len(node.children[i].keys) < t:
                self._fill(node, i)
            if i > len(node.keys):
                self._delete(node.children[i-1], key)
            else:
                self._delete(node.children[i], key)

    def _merge(self, parent: BTreeNode, idx: int) -> None:
        child = parent.children[idx]
        sibling = parent.children[idx+1]
        child.keys.append(parent.keys.pop(idx))
        child.values.append(parent.values.pop(idx))
        child.keys.extend(sibling.keys)
        child.values.extend(sibling.values)
        if not child.leaf:
            child.children.extend(sibling.children)
        parent.children.pop(idx+1)

    def _fill(self, parent: BTreeNode, idx: int) -> None:
        t = self.t
        if idx > 0 and len(parent.children[idx-1].keys) >= t:
            self._borrow_from_prev(parent, idx)
        elif idx < len(parent.children)-1 and len(parent.children[idx+1].keys) >= t:
            self._borrow_from_next(parent, idx)
        else:
            if idx < len(parent.children)-1:
                self._merge(parent, idx)
            else:
                self._merge(parent, idx-1)

    def _borrow_from_prev(self, parent: BTreeNode, idx: int) -> None:
        child = parent.children[idx]
        left_sib = parent.children[idx-1]
        child.keys.insert(0, parent.keys[idx-1])
        child.values.insert(0, parent.values[idx-1])
        if not child.leaf:
            child.children.insert(0, left_sib.children.pop())
        parent.keys[idx-1] = left_sib.keys.pop()
        parent.values[idx-1] = left_sib.values.pop()

    def _borrow_from_next(self, parent: BTreeNode, idx: int) -> None:
        child = parent.children[idx]
        right_sib = parent.children[idx+1]
        child.keys.append(parent.keys[idx])
        child.values.append(parent.values[idx])
        if not child.leaf:
            child.children.append(right_sib.children.pop(0))
        parent.keys[idx] = right_sib.keys.pop(0)
        parent.values[idx] = right_sib.values.pop(0)

    def build_from(self, items: Iterable[Any]) -> "BTree":
        for x in items:
            self.insert(x)
        return self

def main() -> None:
    bt = BTree(t=3).build_from([10, 20, 5, 6, 12, 30, 7, 17])
    print("BTree search 6:", bt.search(6))
    bt.delete(6); print("BTree delete 6, search:", bt.search(6))
    bt.delete(12); print("BTree delete 12, search:", bt.search(12))
    bt.delete(10); print("BTree delete 10, search:", bt.search(10))

if __name__ == "__main__":
    main()
