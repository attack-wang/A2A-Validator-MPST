"""Budget Tracker - monitor expenses and savings."""
from storage import load_data, save_data
from tracker import BudgetTracker

MENU = """
=== Budget Tracker ===
1) Add expense
2) Add income
3) List transactions
4) Delete transaction
5) Set category budget
6) View budgets
7) Set savings goal
8) Summary & savings progress
9) Monthly report
0) Save & exit
"""


def fmt(x):
    return f"${x:,.2f}"


def ask_amount(prompt):
    while True:
        try:
            v = float(input(prompt).strip())
        except ValueError:
            print("Enter a valid number.")
            continue
        if v <= 0:
            print("Amount must be positive.")
            continue
        return v


def ask_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Value cannot be empty.")


def show_txs(tracker):
    if not tracker.transactions:
        print("No transactions recorded.")
        return
    for t in tracker.transactions:
        print(f"  [{t.id}] {t.date}  {t.tx_type.upper():7} {t.category:<15} {fmt(t.amount):>12}  {t.note}")


def add_tx(tracker, tx_type):
    amount = ask_amount("Amount: ")
    category = ask_nonempty("Category: ")
    note = input("Note (optional): ").strip()
    t = tracker.add_transaction(amount, category, tx_type, note)
    print(f"Added {tx_type} [{t.id}].")


def delete_tx(tracker):
    show_txs(tracker)
    tid = input("Transaction ID to delete: ").strip()
    print("Deleted." if tracker.remove_transaction(tid) else "ID not found.")


def set_budget(tracker):
    cat = ask_nonempty("Category: ")
    lim = ask_amount("Monthly limit: ")
    tracker.set_budget(cat, lim)
    print(f"Budget for {cat} set to {fmt(lim)}.")


def set_goal(tracker):
    goal = ask_amount("Savings goal: ")
    tracker.set_savings_goal(goal)
    print(f"Savings goal set to {fmt(goal)}.")


def show_summary(tracker):
    income, expenses, net = tracker.totals()
    print(f"\nIncome:      {fmt(income)}")
    print(f"Expenses:    {fmt(expenses)}")
    print(f"Net savings: {fmt(net)}")
    saved, goal, pct = tracker.savings_progress()
    if goal > 0:
        bar = "#" * int(pct // 5)
        print(f"Goal {fmt(goal)}: saved {fmt(saved)} ({pct:.1f}%) [{bar:<20}]")


def show_budgets(tracker):
    status = tracker.budget_status()
    if not status:
        print("No budgets set. Use 'Set category budget' first.")
        return
    for cat, s in status.items():
        flag = "OVER!" if s["remaining"] < 0 else "ok"
        print(f"  {cat:<15} limit {fmt(s['limit']):>10} spent {fmt(s['spent']):>10} "
              f"remaining {fmt(s['remaining']):>10} [{flag}]")


def show_report(tracker):
    month = input("Month (YYYY-MM, blank for all): ").strip() or None
    income, expenses, net, rows = tracker.monthly_report(month)
    print(f"\nReport for {month or 'all time'}")
    print(f"  Income:   {fmt(income)}")
    print(f"  Expenses: {fmt(expenses)}")
    print(f"  Net:      {fmt(net)}")
    cats = tracker.category_expenses(rows)
    if cats:
        print("  Spending by category:")
        for cat, amt in sorted(cats.items(), key=lambda kv: -kv[1]):
            print(f"    {cat:<15} {fmt(amt):>10}")


def main():
    tracker = BudgetTracker(load_data())
    actions = {
        "1": lambda: add_tx(tracker, "expense"),
        "2": lambda: add_tx(tracker, "income"),
        "3": lambda: show_txs(tracker),
        "4": lambda: delete_tx(tracker),
        "5": lambda: set_budget(tracker),
        "6": lambda: show_budgets(tracker),
        "7": lambda: set_goal(tracker),
        "8": lambda: show_summary(tracker),
        "9": lambda: show_report(tracker),
    }
    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "0":
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid option.")
    except (EOFError, KeyboardInterrupt):
        # End of input (e.g. closed stdin or Ctrl+C): save and exit cleanly.
        pass
    save_data(tracker.persist())
    print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()