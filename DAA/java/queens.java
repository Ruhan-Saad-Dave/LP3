public class queens {
    static final int N = 8;
    static int[][] board = new int[N][N];

    static boolean safe(int r, int c) {
        for (int i = 0; i < r; i++) {
            if (board[i][c] == 1 ||
                (c - r + i >= 0 && board[i][c - r + i] == 1) ||
                (c + r - i < N && board[i][c + r - i] == 1))
                return false;
        }
        return true;
    }

    static boolean solve(int r) {
        if (r == N) return true;

        for (int c = 0; c < N; c++) {
            if (safe(r, c)) {
                board[r][c] = 1;

                if (solve(r + 1)) return true;

                board[r][c] = 0;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        board[0][0] = 1;
        solve(1);

        for (int[] row : board) {
            for (int x : row)
                System.out.print(x + " ");
            System.out.println();
        }
    }
}