N = 8
board = [[0] * N for _ in range(N)]

def safe(r, c):
    for i in range(r):
        if board[i][c] or (c-r+i >= 0 and board[i][c-r+i]) or (c+r-i < N and board[i][c+r-i]):
            return False
    return True

def solve(r):
    if r == N:
        return True
    for c in range(N):
        if safe(r, c):
            board[r][c] = 1
            if solve(r + 1):
                return True
            board[r][c] = 0
    return False

board[0][0] = 1
solve(1)

for row in board:
    print(*row)