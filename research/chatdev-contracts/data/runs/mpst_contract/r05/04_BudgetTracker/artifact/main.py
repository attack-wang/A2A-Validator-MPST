"""Budget Tracker - monitor expenses and savings."""
import datetime

from tracker import BudgetTracker


def fmt(x):
    return f"${x:,.2f}"


def read_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value <= 0:
                print("Amount must be positive.")
                continue
            return value
        except ValueError:
            print("Enter a valid number.")


def read_date(prompt):
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return datetime.date.fromisoformat(raw).isoformat()
    except ValueError:
        print("Invalid date; using today.")
        return None


def show_transactions(txns):
    if not txns:
        print("No transactions recorded.")
        return
    print(f"\n{'ID':>4} {'Date':<12} {'Type':<8} {'Category':<15} "
          f"{'Description':<25} {'Amount':>10}")
    print("-" * 78)
    for t in txns:
        print(f"{t.id:>4} {t.date:<12} {t.ttype:<8} {t.category:<15} "
              f"{t.description[:25]:<25} {fmt(t.amount):>10}")


def main():
    app = BudgetTracker()
    menu = (
        "\n=== Budget Tracker ===\n"
        "1) Add expense\n"
        "2) Add income\n"
        "3) List transactions\n"
        "4) Delete transaction\n"
        "5) Monthly summary\n"
        "6) Category breakdown\n"
        "7) Add savings goal\n"
        "8) View savings goals\n"
        "9) Contribute to goal\n"
        "10) Exit"
    )
    while True:
        print(menu)
        choice = input("Select option: ").strip()
        try:
            if choice == "1":
                date = read_date("Date (YYYY-MM-DD, blank=today): ")
                t = app.add_transaction(
                    "expense", read_float("Amount: "),
                    input("Category: ").strip() or "Uncategorized",
                    input("Description: ").strip(), date)
                print(f"Expense #{t.id} recorded.")
            elif choice == "2":
                date = read_date("Date (YYYY-MM-DD, blank=today): ")
                t = app.add_transaction(
                    "income", read_float("Amount: "),
                    input("Source: ").strip() or "Income",
                    input("Description: ").strip(), date)
                print(f"Income #{t.id} recorded.")
            elif choice == "3":
                month = input("Filter month YYYY-MM (blank=all): ").strip() or None
                show_transactions(app.transactions(month))
            elif choice == "4":
                txn_id = int(input("Transaction ID to delete: ").strip())
                print("Deleted." if app.delete_transaction(txn_id) else "ID not found.")
            elif choice == "5":
                month = input("Month YYYY-MM (blank=all): ").strip() or None
                income, expenses, net = app.summary(month)
                print(f"\nSummary ({month or 'All time'}): "
                      f"Income {fmt(income)} | Expenses {fmt(expenses)} | Net {fmt(net)}")
            elif choice == "6":
                month = input("Month YYYY-MM (blank=all): ").strip() or None
                breakdown = app.category_breakdown(month)
                if not breakdown:
                    print("No expenses recorded.")
                else:
                    total = sum(breakdown.values())
                    print(f"\n{'Category':<20}{'Amount':>12}{'Share':>10}")
                    for cat, amt in breakdown.items():
                        print(f"{cat:<20}{fmt(amt):>12}{amt / total * 100:>9.1f}%")
            elif choice == "7":
                name = input("Goal name: ").strip()
                target = read_float("Target amount: ")
                g = app.add_goal(name, target)
                print(f"Goal '{g.name}' created with target {fmt(g.target)}.")
            elif choice == "8":
                goals = app.goals()
                if not goals:
                    print("No savings goals yet.")
                else:
                    for g in goals:
                        pct = g.saved / g.target * 100 if g.target else 0
                        print(f"{g.name}: {fmt(g.saved)} / {fmt(g.target)} ({pct:.1f}%)")
                    print(f"Total saved: {fmt(app.total_saved())}")
            elif choice == "9":
                name = input("Goal name: ").strip()
                amount = read_float("Amount to add: ")
                g = app.contribute(name, amount)
                pct = g.saved / g.target * 100 if g.target else 0
                print(f"{g.name}: {fmt(g.saved)} / {fmt(g.target)} ({pct:.1f}%)")
            elif choice == "10":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()