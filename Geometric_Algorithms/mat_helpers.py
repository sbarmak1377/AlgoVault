from typing import List, Iterable
import math

Matrix = List[List[float]]
Vec = List[float]

def mat_mul(A: Matrix, B: Matrix) -> Matrix:
    """Matrix multiply (naive)."""
    n, k, m = len(A), len(A[0]), len(B[0])
    assert k == len(B)
    C = [[0.0]*m for _ in range(n)]
    for i in range(n):
        for t in range(k):
            a = A[i][t]
            if a == 0: 
                continue
            for j in range(m):
                C[i][j] += a * B[t][j]
    return C

def mat_vec_mul(A: Matrix, v: Vec) -> Vec:
    """Multiply matrix by vector."""
    return [sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A))]

def pretty(M: Matrix) -> str:
    return "\\n".join("[" + ", ".join(f\"{x:.4f}\" for x in row) + "]" for row in M)
