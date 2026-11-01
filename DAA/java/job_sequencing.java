import java.util.*;

public class job_sequencing {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        int[][] jobs = new int[n][3];

        for (int i = 0; i < n; i++) {
            jobs[i][0] = i + 1;
            jobs[i][1] = sc.nextInt();
            jobs[i][2] = sc.nextInt();
        }

        Arrays.sort(jobs, (a, b) -> b[2] - a[2]);

        int[] slots = new int[n + 1];
        int profit = 0;

        for (int[] job : jobs) {
            for (int j = Math.min(job[1], n); j > 0; j--) {
                if (slots[j] == 0) {
                    slots[j] = job[0];
                    profit += job[2];
                    break;
                }
            }
        }

        System.out.println("Scheduled Jobs: " +
                Arrays.toString(Arrays.copyOfRange(slots, 1, n + 1)));
        System.out.println("Maximum Profit: " + profit);
        sc.close();
    }
}