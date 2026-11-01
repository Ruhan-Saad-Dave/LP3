n = int(input())
jobs = []

for i in range(n):
    d, p = map(int, input().split())
    jobs.append((i + 1, d, p))

jobs.sort(key=lambda x: x[2], reverse=True)

slots = [0] * (n + 1)
profit = 0

for i, d, p in jobs:
    for j in range(min(d, n), 0, -1):
        if slots[j] == 0:
            slots[j] = i
            profit += p
            break

print("Scheduled Jobs:", slots[1:])
print("Maximum Profit:", profit)