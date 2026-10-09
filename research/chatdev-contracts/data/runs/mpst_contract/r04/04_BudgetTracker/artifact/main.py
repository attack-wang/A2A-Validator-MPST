from budget import BudgetTracker
from storage import load, save, DEFAULT_FILE


def ask_amount(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Amount must be positive.")
        except ValueError:
            print("Enter a valid number.")


def ask_nonempty(prompt, default=""):
    text = input(prompt).strip()
    return text or default


def add_transaction(tracker, kind):
    label = "expense" if kind == "expense" else "income / savings deposit"
    print(f"\n--- Add {label} ---")
    category = ask_nonempty("Category (e.g. Food, Rent, Salary): ", "Uncategorized")
    amount = ask_amount("Amount: ")
    note = input("Note (optional): ").strip()
    t = tracker.add(kind, category, amount, note)
    print(f"Added {kind} #{t.tid}: {t.category} ${t.amount:.2f}")


def list_transactions(tracker):
    print("\n--- Transactions ---")
    if not tracker.transactions:
        print("No transactions recorded yet.")
        return
    for t in tracker.transactions:
        sign = "-" if t.kind == "expense" else "+"
        print(f"[{t.tid}] {t.date} {sign}${t.amount:>9.2f}  {t.kind:<7} {t.category:<15} {t.note}")


def show_summary(tracker):
    print("\n--- Summary ---")
    print(f"Total income : ${tracker.total('income'):.2f}")
    print(f"Total expense: ${tracker.total('expense'):.2f}")
    print(f"Savings      : ${tracker.balance():.2f}")
    print(f"Savings rate : {tracker.savings_rate():.1f}%")
    for kind, title in (("expense", "Expenses by category"), ("income", "Income by category")):
        cats = tracker.by_category(kind)
        if cats:
            print(f"\n{title}:")
            for cat, amt in cats.items():
                print(f"  {cat:<15} ${amt:.2f}")


def delete_transaction(tracker):
    tid = input("Enter transaction ID to delete: ").strip()
    removed = tracker.remove(tid)
    print(f"Deleted #{tid}." if removed else f"No transaction with ID {tid}.")


def save_now(tracker):
    save(tracker)
    print(f"Saved to {DEFAULT_FILE}.")


MENU = """
====== Budget Tracker ======
1) Add expense
2) Add income / savings deposit
3) List transactions
4) Show summary
5) Delete transaction
6) Save now
0) Exit
"""


def main():
    tracker = load()
    print(f"Loaded {len(tracker.transactions)} transaction(s) from {DEFAULT_FILE}.")
    actions = {
        "1": lambda: add_transaction(tracker, "expense"),
        "2": lambda: add_transaction(tracker, "income"),
        "3": lambda: list_transactions(tracker),
        "4": lambda: show_summary(tracker),
        "5": lambda: delete_transaction(tracker),
        "6": lambda: save_now(tracker),
    }
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            save(tracker)
            print(f"Saved to {DEFAULT_FILE}. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()