def fib_dp(n: int) -> int:
    """Bottom-up dynamic programming Fibonacci. O(n) time / O(1) space."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def main():
    print("Fibonacci DP")
    for i in range(10):
        print(i, fib_dp(i))

if __name__ == "__main__":
    main()
