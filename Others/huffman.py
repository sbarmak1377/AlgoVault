from typing import Dict, Optional, Tuple, List
import heapq

class Node:
    def __init__(self, freq: int, ch: Optional[str]=None, left: 'Node'=None, right: 'Node'=None):
        self.freq, self.ch, self.left, self.right = freq, ch, left, right
    def __lt__(self, other: 'Node'):
        return self.freq < other.freq

def build_huffman(freqs: Dict[str, int]) -> Node:
    pq = [Node(f, ch) for ch, f in freqs.items()]
    heapq.heapify(pq)
    if len(pq) == 1:
        # Edge case: single symbol
        only = pq[0]
        return Node(only.freq, None, only, None)
    while len(pq) > 1:
        a = heapq.heappop(pq)
        b = heapq.heappop(pq)
        heapq.heappush(pq, Node(a.freq + b.freq, None, a, b))
    return pq[0]

def build_code_table(root: Node) -> Dict[str, str]:
    table: Dict[str, str] = {}
    def dfs(n: Node, pref: str):
        if n.ch is not None:
            table[n.ch] = pref or "0"
            return
        if n.left: dfs(n.left, pref + "0")
        if n.right: dfs(n.right, pref + "1")
    dfs(root, "")
    return table

def encode(s: str, table: Dict[str, str]) -> str:
    return "".join(table[ch] for ch in s)

def decode(bits: str, root: Node) -> str:
    out: List[str] = []
    node = root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.ch is not None:
            out.append(node.ch)
            node = root
    return "".join(out)

def main():
    text = "huffman coding example"
    # frequency table
    freqs: Dict[str, int] = {}
    for ch in text:
        freqs[ch] = freqs.get(ch, 0) + 1
    root = build_huffman(freqs)
    table = build_code_table(root)
    bits = encode(text, table)
    recovered = decode(bits, root)
    print("table (partial):", dict(list(table.items())[:5]))
    print("encoded length:", len(bits), "bits")
    print("decoded equals original?", recovered == text)

if __name__ == "__main__":
    main()
