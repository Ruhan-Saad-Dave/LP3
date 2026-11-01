n = int(input())
capacity = int(input())

items = [tuple(map(int, input().split())) for _ in range(n)]
items.sort(key=lambda x: x[0] / x[1], reverse=True)

profit = 0

for p, w in items:
    if capacity >= w:
        profit += p
        capacity -= w
    else:
        profit += p * capacity / w
        break

print("Maximum Profit:", round(profit, 2))