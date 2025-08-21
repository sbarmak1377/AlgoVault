from __future__ import annotations
from typing import Dict, Iterable, Iterator, List, Tuple, TypeVar, Generic, Optional, Set

# Generic Type used to store any type of data in graph nodes.
T = TypeVar("T")

class Graph(Generic[T]):
    def __init__(self, directed: bool) -> None:
        self._directed = directed
        self._adj: Dict[T, Dict[T, float]] = {}

    @property
    def directed(self) -> bool:
        return self._directed

    def add_node(self, u: T) -> None:
        if u not in self._adj:
            self._adj[u] = {}

    def add_edge(self, u: T, v: T, weight: float = 1.0) -> None:
        self.add_node(u); self.add_node(v)
        self._adj[u][v] = weight
        if not self._directed:
            self._adj[v][u] = weight

    def add_edges_from(self, edges: Iterable[Tuple[T, T, float]]) -> None:
        for u, v, w in edges:
            self.add_edge(u, v, w)

    def neighbors(self, u: T) -> Dict[T, float]:
        return self._adj.get(u, {})

    def nodes(self) -> List[T]:
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[T, T, float]]:
        if self._directed:
            return [(u, v, w) for u, nbrs in self._adj.items() for v, w in nbrs.items()]
        seen = set()
        out = []
        for u, nbrs in self._adj.items():
            for v, w in nbrs.items():
                a, b = (u, v) if str(u) <= str(v) else (v, u)
                if (a, b) in seen: 
                    continue
                seen.add((a, b))
                out.append((a, b, w))
        return out

    def undirected_view_neighbors(self, u: T):
        seen = set()
        for v, w in self._adj.get(u, {}).items():
            seen.add(v)
            yield (v, w)
        if self._directed:
            for x, nbrs in self._adj.items():
                if x == u: 
                    continue
                w = nbrs.get(u)
                if w is not None and x not in seen:
                    yield (x, w)

    def __repr__(self) -> str:
        typ = "Directed" if self._directed else "Undirected"
        return f"{typ}Graph(|V|={len(self._adj)})"
