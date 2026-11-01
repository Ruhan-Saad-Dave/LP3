import java.util.*;

public class knapsack {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int capacity = sc.nextInt();

        int[][] items = new int[n][2];

        for (int i = 0; i < n; i++) {
            items[i][0] = sc.nextInt();
            items[i][1] = sc.nextInt();
        }

        int[] dp = new int[capacity + 1];

        for (int[] item : items) {
            int p = item[0], w = item[1];

            for (int j = capacity; j >= w; j--) {
                dp[j] = Math.max(dp[j], dp[j - w] + p);
            }
        }

        System.out.println("Maximum Profit: " + dp[capacity]);
        sc.close();
    }
}