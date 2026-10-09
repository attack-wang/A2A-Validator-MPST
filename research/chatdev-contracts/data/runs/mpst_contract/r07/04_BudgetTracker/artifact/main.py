from tracker import BudgetTracker


def fmt(x):
    return f"${x:,.2f}"


def read_line(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        print()
        return None
    except KeyboardInterrupt:
        print()
        return None


def read_amount(prompt):
    while True:
        line = read_line(prompt)
        if line is None:
            return None
        try:
            v = float(line.strip())
            if v > 0:
                return v
            print("Amount must be positive.")
        except ValueError:
            print("Enter a valid number.")


def read_nonempty(prompt):
    s = read_line(prompt)
    if s is None:
        return None
    s = s.strip()
    return s or "General"


def add_income(tracker):
    cat = read_nonempty("Income source (e.g. Salary): ")
    if cat is None:
        print("Cancelled.")
        return
    amt = read_amount("Amount: ")
    if amt is None:
        print("Cancelled.")
        return
    note = read_line("Note (optional): ")
    t = tracker.add("income", cat, amt, (note or "").strip())
    print(f"Added income {fmt(t.amount)} from {t.category}.")


def add_expense(tracker):
    cat = read_nonempty("Expense category (e.g. Food): ")
    if cat is None:
        print("Cancelled.")
        return
    amt = read_amount("Amount: ")
    if amt is None:
        print("Cancelled.")
        return
    note = read_line("Note (optional): ")
    t = tracker.add("expense", cat, amt, (note or "").strip())
    print(f"Added expense {fmt(t.amount)} for {t.category}.")


def show_transactions(tracker):
    txns = tracker.list_transactions()
    if not txns:
        print("\nNo transactions recorded yet.")
        return
    print("\n--- Transactions ---")
    for i, t in enumerate(txns, 1):
        print(f"{i:>3}. [{t['date']}] {t['kind'].upper():<7} "
              f"{t['category']:<15} {fmt(t['amount']):>10}  {t['note']}")


def remove_transaction(tracker):
    show_transactions(tracker)
    if not tracker.list_transactions():
        return
    idx = read_line("Number to remove (blank to cancel): ")
    if not idx:
        return
    try:
        removed = tracker.remove(int(idx.strip()) - 1)
        if removed:
            print(f"Removed: {removed['kind']} {removed['category']} {fmt(removed['amount'])}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")


def set_goal(tracker):
    amt = read_amount("Savings goal amount: ")
    if amt is None:
        print("Cancelled.")
        return
    tracker.set_goal(amt)
    print(f"Savings goal set to {fmt(amt)}.")


def show_summary(tracker):
    income, expenses, balance = tracker.totals()
    print("\n--- Summary ---")
    print(f"Total income:   {fmt(income)}")
    print(f"Total expenses: {fmt(expenses)}")
    print(f"Net balance:    {fmt(balance)}")
    saved, goal, pct = tracker.savings_progress()
    if goal > 0:
        bar = "#" * int(pct // 5)
        print(f"Savings goal:   {fmt(goal)} | Saved: {fmt(saved)} "
              f"({pct:.1f}%) [{bar:<20}]")
    cats = tracker.by_category()
    if cats:
        print("Expenses by category:")
        for c, a in sorted(cats.items(), key=lambda kv: -kv[1]):
            print(f"  {c:<15} {fmt(a)}")


def main():
    tracker = BudgetTracker()
    actions = {
        "1": ("Add income", add_income),
        "2": ("Add expense", add_expense),
        "3": ("View transactions", show_transactions),
        "4": ("Remove transaction", remove_transaction),
        "5": ("Set savings goal", set_goal),
        "6": ("Summary", show_summary),
    }
    print("Welcome to the Budget Tracker!")
    while True:
        print("\nMenu:")
        for k, (label, _) in actions.items():
            print(f"  {k}) {label}")
        print("  7) Exit")
        choice = read_line("Choose an option: ")
        if choice is None:
            print("\nInput closed. Goodbye! Your data is saved.")
            break
        choice = choice.strip()
        if choice == "7":
            print("Goodbye! Your data is saved.")
            break
        action = actions.get(choice)
        if action:
            action[1](tracker)
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()