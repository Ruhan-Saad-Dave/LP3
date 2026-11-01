"""
=============================================================================
Assignment: DAA (Index Sr 2 / Alternate DAA2)
Title: Implement Job Sequencing with Deadlines using a Greedy method.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""


class Job:
    """Represents a job with an ID, deadline, and profit."""
    def __init__(self, job_id, deadline, profit):
        self.job_id = job_id
        self.deadline = deadline
        self.profit = profit


def job_sequencing_greedy(jobs):
    """
    Schedules jobs to maximize total profit such that each job completes 
    within its deadline. Each job takes 1 unit of time.
    
    Greedy Strategy:
      1. Sort all jobs in descending order of their profit.
      2. For each job, find the latest available time slot <= deadline.
      3. If a free slot is found, schedule the job in that slot.
      
    Time Complexity:
      - Sorting jobs by profit: O(n log n)
      - Slot allocation: O(n * d_max) where d_max is maximum deadline.
      - Total Time Complexity: O(n log n + n * d_max) (or O(n^2) in worst case).
    Space Complexity:
      - Slot array: O(d_max)
    """
    # Step 1: Sort jobs in descending order of profit
    jobs.sort(key=lambda x: x.profit, reverse=True)

    # Step 2: Determine maximum deadline to determine total time slots
    max_deadline = max(job.deadline for job in jobs) if jobs else 0

    # Slots array: index 0 is unused, slots 1..max_deadline
    # slot[t] = None indicates slot t is free
    slots = [None] * (max_deadline + 1)

    total_profit = 0
    scheduled_jobs = []

    print("\n--- Greedy Step-by-Step Scheduling ---")
    print(f"{'Job ID':<8} | {'Deadline':<10} | {'Profit':<8} | {'Assigned Slot':<15} | {'Status':<10}")
    print("-" * 60)

    for job in jobs:
        # Search for a free slot from min(max_deadline, job.deadline) down to 1
        allocated = False
        for t in range(min(max_deadline, job.deadline), 0, -1):
            if slots[t] is None:
                slots[t] = job
                total_profit += job.profit
                scheduled_jobs.append(job)
                allocated = True
                print(f"{job.job_id:<8} | {job.deadline:<10} | {job.profit:<8} | {f'Slot {t-1} - {t}':<15} | Scheduled")
                break
        if not allocated:
            print(f"{job.job_id:<8} | {job.deadline:<10} | {job.profit:<8} | {'None':<15} | Rejected")

    return total_profit, slots, scheduled_jobs


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("=" * 70)
    print(" DAA Assignment: Job Sequencing with Deadlines (Greedy Method)")
    print("=" * 70)

    print("Choose mode:")
    print("  1. Run standard practical exam benchmark [Default]")
    print("  2. Enter custom jobs")
    choice = safe_input("Enter choice (1/2) [Default: 1]: ", "1")

    if choice == "2":
        try:
            n = int(safe_input("Enter number of jobs (n): ", "5"))
            jobs = []
            for i in range(1, n + 1):
                jid = safe_input(f"  Job {i} - Enter Job ID (e.g., J{i}): ", f"J{i}")
                dl = int(safe_input(f"  Job {i} - Enter Deadline: ", "2"))
                pr = int(safe_input(f"  Job {i} - Enter Profit: ", "50"))
                jobs.append(Job(jid, dl, pr))
        except ValueError:
            print("Invalid input! Falling back to standard dataset.")
            jobs = [
                Job("J1", 2, 100),
                Job("J2", 1, 19),
                Job("J3", 2, 27),
                Job("J4", 1, 25),
                Job("J5", 3, 15),
            ]
    else:
        # Standard benchmark problem
        jobs = [
            Job("J1", 2, 100),
            Job("J2", 1, 19),
            Job("J3", 2, 27),
            Job("J4", 1, 25),
            Job("J5", 3, 15),
        ]

    print("\n" + "-" * 50)
    print("INPUT JOBS LIST:")
    print("-" * 50)
    print(f"{'Job ID':<10} | {'Deadline':<12} | {'Profit':<10}")
    print("-" * 50)
    for j in jobs:
        print(f"{j.job_id:<10} | {j.deadline:<12} | {j.profit:<10}")
    print("-" * 50)

    total_profit, slots, scheduled = job_sequencing_greedy(jobs)

    print("\n" + "=" * 60)
    print("                 OPTIMAL JOB SCHEDULE")
    print("=" * 60)
    execution_order = [slots[t].job_id for t in range(1, len(slots)) if slots[t] is not None]
    print(f"Scheduled Job Sequence : {' -> '.join(execution_order)}")
    print(f"Total Profit Earned    : {total_profit} units")
    print(f"Total Jobs Scheduled   : {len(scheduled)} / {len(jobs)}")
    print("-" * 60)
    print("Time Complexity        : O(n log n + n * d_max)")
    print("Space Complexity       : O(d_max) for time slot array")
    print("=" * 60)


if __name__ == "__main__":
    main()
