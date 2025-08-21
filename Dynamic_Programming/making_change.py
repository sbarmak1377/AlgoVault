from typing import List, Tuple

def min_coins(amount: int, coins: List[int]) -> Tuple[int, List[int]]:
    """
    Unbounded coin change (min coins). Returns (min_count, combination).
    O(amount * len(coins)) time, O(amount) space.
    """
    INF = 10**9
    dp = [0] + [INF] * amount
    prev = [-1] * (amount + 1)
    coin_choice = [-1] * (amount + 1)
    for a in range(1, amount + 1):
        best = INF
        chosen = -1
        for c in coins:
            if c <= a and dp[a - c] + 1 < best:
                best = dp[a - c] + 1
                chosen = c
        dp[a] = best
        coin_choice[a] = chosen
        if chosen != -1:
            prev[a] = a - chosen
    if dp[amount] >= INF:
        return (float("inf"), [])
    # Reconstruct
    comb = []
    cur = amount
    while cur > 0 and coin_choice[cur] != -1:
        comb.append(coin_choice[cur])
        cur -= coin_choice[cur]
    return dp[amount], comb

def main():
    print("Making Change (min coins)")
    amount = 27
    coins = [1, 5, 10, 25]
    cnt, comb = min_coins(amount, coins)
    print(f"amount={amount}, coins={coins} -> min={cnt}, example={comb}")

if __name__ == "__main__":
    main()
