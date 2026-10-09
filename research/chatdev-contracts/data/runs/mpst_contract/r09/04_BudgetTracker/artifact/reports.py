def print_transactions(transactions):
    if not transactions:
        print("No transactions recorded.")
        return
    print(f"{'ID':<10}{'Date':<12}{'Type':<9}{'Category':<15}{'Amount':>10}  Note")
    print("-" * 70)
    for t in sorted(transactions, key=lambda x: x.date, reverse=True):
        print(f"{t.id:<10}{t.date:<12}{t.type:<9}{t.category:<15}"
              f"{t.amount:>10.2f}  {t.note}")


def print_summary(tracker):
    income = tracker.total("income")
    expense = tracker.total("expense")
    print("\n=== Summary ===")
    print(f"Total income : {income:>10.2f}")
    print(f"Total expense: {expense:>10.2f}")
    print(f"Savings      : {tracker.savings():>10.2f}")
    spent = tracker.spent_by_category()
    if spent:
        print("\nExpenses by category:")
        for cat, amt in sorted(spent.items(), key=lambda kv: -kv[1]):
            print(f"  {cat:<15}{amt:>10.2f}")


def print_budgets(tracker):
    status = tracker.budget_status()
    if not status:
        print("No budgets set. Use 'Set category budget' to add one.")
        return
    print(f"\n{'Category':<15}{'Limit':>10}{'Spent':>10}{'Remaining':>12}  Status")
    print("-" * 62)
    for cat, limit, spent in status:
        remaining = round(limit - spent, 2)
        if spent > limit:
            state = "OVER BUDGET"
        elif spent >= limit * 0.8:
            state = "Warning"
        else:
            state = "OK"
        print(f"{cat:<15}{limit:>10.2f}{spent:>10.2f}{remaining:>12.2f}  {state}")