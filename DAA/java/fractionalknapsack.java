import java.util.*;

public class fractionalknapsack {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int capacity = sc.nextInt();

        double[][] items = new double[n][2];

        for (int i = 0; i < n; i++) {
            items[i][0] = sc.nextDouble();
            items[i][1] = sc.nextDouble();
        }

        Arrays.sort(items, (a, b) ->
            Double.compare(b[0] / b[1], a[0] / a[1]));

        double profit = 0;

        for (double[] item : items) {
            double p = item[0], w = item[1];

            if (capacity >= w) {
                profit += p;
                capacity -= w;
            } else {
                profit += p * capacity / w;
                break;
            }
        }

        System.out.printf("Maximum Profit: %.2f%n", profit);
        sc.close();
    }
}