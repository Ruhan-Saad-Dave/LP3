n = int(input())
capacity = int(input())

items = [tuple(map(int, input().split())) for _ in range(n)]

dp = [0] * (capacity + 1)

for p, w in items:
    for j in range(capacity, w - 1, -1):
        dp[j] = max(dp[j], dp[j - w] + p)

print("Maximum Profit:", dp[capacity])