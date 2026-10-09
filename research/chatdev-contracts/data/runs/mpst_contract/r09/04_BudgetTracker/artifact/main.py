from datetime import datetime
from tracker import BudgetTracker
from reports import print_summary, print_transactions, print_budgets

MENU = """
===== Budget Tracker =====
1. Add expense
2. Add income
3. List transactions
4. Delete transaction
5. Set category budget
6. View budgets
7. View summary
8. Exit
"""


def ask_amount(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return round(value, 2)
            print("Amount must be positive.")
        except ValueError:
            print("Enter a valid number.")


def ask_date():
    raw = input("Date (YYYY-MM-DD, blank for today): ").strip()
    if not raw:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        print("Invalid date; using today.")
        return datetime.now().strftime("%Y-%m-%d")


def add_transaction(tracker, ttype):
    category = input("Category: ").strip() or "General"
    amount = ask_amount("Amount: ")
    date = ask_date()
    note = input("Note (optional): ").strip()
    t = tracker.add_transaction(ttype, category, amount, date, note)
    print(f"Added {ttype} {t.id}: {category} {t.amount:.2f} on {t.date}")


def delete_transaction(tracker):
    tid = input("Transaction ID to delete: ").strip()
    print("Deleted." if tracker.remove_transaction(tid) else "ID not found.")


def set_budget(tracker):
    category = input("Budget category: ").strip() or "General"
    limit = ask_amount("Monthly limit: ")
    tracker.set_budget(category, limit)
    print(f"Budget set: {category} limit {limit:.2f}")


def main():
    tracker = BudgetTracker()
    tracker.load()
    actions = {
        "1": lambda: add_transaction(tracker, "expense"),
        "2": lambda: add_transaction(tracker, "income"),
        "3": lambda: print_transactions(tracker.transactions),
        "4": lambda: delete_transaction(tracker),
        "5": lambda: set_budget(tracker),
        "6": lambda: print_budgets(tracker),
        "7": lambda: print_summary(tracker),
    }
    while True:
        print(MENU)
        choice = input("Select option: ").strip()
        if choice == "8":
            print("Goodbye! Data saved.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()