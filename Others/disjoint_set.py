from typing import Any, Dict

class DisjointSet:
    """Union–Find with path compression and union by rank."""
    def __init__(self):
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}

    def find(self, x: Any) -> Any:
        if self.parent.get(x, x) != x:
            self.parent[x] = self.find(self.parent[x])
        else:
            self.parent.setdefault(x, x)
        self.rank.setdefault(x, 0)
        return self.parent[x]

    def union(self, a: Any, b: Any) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

def main():
    ds = DisjointSet()
    for x in range(1, 7): ds.find(x)
    ds.union(1,2); ds.union(2,3); ds.union(4,5)
    print("find(1)==find(3)?", ds.find(1)==ds.find(3))
    print("find(1)==find(4)?", ds.find(1)==ds.find(4))
    ds.union(3,4)
    print("After union(3,4): find(1)==find(5)?", ds.find(1)==ds.find(5))

if __name__ == "__main__":
    main()
