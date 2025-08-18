from typing import List

def factorial(n: int) -> int:
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def reverse_string_v1(string: str) -> str:
    if len(string) == 1:
        return string
    else:
        return string[-1] + reverse_string_v1(string[:-1])

def reverse_string_v2(string: str) -> str:
    if len(string) == 1:
        return string
    else:
        return reverse_string_v2(string[1:]) + string[0]


def reverse_string_v3(s: str) -> str:
    """
    Recursive in-place (via list) two-pointer swap.
    O(n) time, O(n) extra space (list + recursion stack).
    """
    chars = list(s)

    def rec(i: int, j: int):
        if i >= j:
            return
        chars[i], chars[j] = chars[j], chars[i]
        rec(i + 1, j - 1)

    rec(0, len(chars) - 1)
    return "".join(chars)


def solve_n_queens(n: int):
    solutions = []
    # -1 means not placed yet
    place = [-1] * n

    def safe(row: int, col: int) -> bool:
        for r in range(row):
            c = place[r]
            # same column
            if c == col:
                return False
            # same diagonal
            if abs(row - r) == abs(col - c):
                return False
        return True

    def backtrack(row: int):
        # we iterate from 0 to n-1 row
        if row == n:
            solutions.append(place.copy())
            return
        for col in range(n):
            if safe(row, col):
                place[row] = col
                backtrack(row + 1)
                place[row] = -1  # undo

    backtrack(0)
    return solutions


# ---------- N-Queens ----------
def solve_n_queens_gpt_solution(n: int) -> List[List[int]]:
    """
    Returns all solutions as lists of column indices per row, e.g. [1,3,0,2].
    Uses your 'place' array idea; adds simple validation and optional O(1) safety checks.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    solutions: List[List[int]] = []
    place = [-1] * n

    # Optional speed-ups: track used cols/diagonals in O(1)
    used_cols = set()
    used_diag1 = set()  # r - c
    used_diag2 = set()  # r + c

    def safe(row: int, col: int) -> bool:
        # With sets this is O(1); keep your original logic as comments for clarity:
        # for r in range(row):
        #     c = place[r]
        #     if c == col or abs(row - r) == abs(col - c):
        #         return False
        # return True
        return (
            col not in used_cols and
            (row - col) not in used_diag1 and
            (row + col) not in used_diag2
        )

    def backtrack(row: int):
        if row == n:
            solutions.append(place.copy())
            return
        for col in range(n):
            if safe(row, col):
                place[row] = col
                used_cols.add(col)
                used_diag1.add(row - col)
                used_diag2.add(row + col)

                backtrack(row + 1)

                used_cols.remove(col)
                used_diag1.remove(row - col)
                used_diag2.remove(row + col)
                place[row] = -1

    backtrack(0)
    return solutions

def main():
    print(f"Factorial of 5: {factorial(5)}")
    test_str = 'ABCDEF'
    print(f"Reverse of {test_str} V1 Code: {reverse_string_v1(test_str)}")
    print(f"Reverse of {test_str} V2 Code: {reverse_string_v2(test_str)}")
    print(solve_n_queens(4))



if __name__ == '__main__':
    main()