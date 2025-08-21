from typing import List, Tuple

def lcs(a: str, b: str) -> Tuple[int, str]:
    """Classic LCS DP with reconstruction. O(n*m) time, O(n*m) space."""
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = dp[i-1][j] if dp[i-1][j] >= dp[i][j-1] else dp[i][j-1]
    # reconstruct
    i, j = n, m
    out: List[str] = []
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            out.append(a[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    out.reverse()
    return dp[n][m], "".join(out)

def main():
    s1, s2 = "dynamic", "algorithmic"
    length, subseq = lcs(s1, s2)
    print(f"LCS('{s1}', '{s2}') length={length}, subseq='{subseq}'")

if __name__ == "__main__":
    main()
