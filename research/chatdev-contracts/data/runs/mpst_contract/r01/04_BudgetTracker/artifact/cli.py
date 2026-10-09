from tracker import BudgetTracker


def fmt_money(value):
    return f"${value:,.2f}"


def print_transactions(tracker):
    txs = tracker.list_transactions()
    if not txs:
        print("No transactions recorded yet.")
        return
    print(f"\n{'#':>3}  {'Date':<17}{'Type':<9}{'Category':<15}{'Amount':>12}  Note")
    print("-" * 78)
    for i, t in enumerate(txs, 1):
        print(f"{i:>3}  {t['date']:<17}{t['type']:<9}{t['category']:<15}"
              f"{fmt_money(t['amount']):>12}  {t['note']}")


def print_summary(tracker):
    s = tracker.summary()
    print("\n=== Summary ===")
    print(f"Total Income  : {fmt_money(s['income'])}")
    print(f"Total Expenses: {fmt_money(s['expenses'])}")
    print(f"Total Savings : {fmt_money(s['savings'])}")
    print(f"Net Balance   : {fmt_money(s['balance'])}")
    breakdown = tracker.category_breakdown()
    if breakdown:
        print("\nExpenses by Category:")
        for cat, amt in breakdown.items():
            print(f"  {cat:<15}{fmt_money(amt):>12}")


def prompt_float(msg):
    while True:
        try:
            value = float(input(msg).strip())
            if value > 0:
                return value
            print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid number.")


def run_cli(tracker):
    menu = (
        "\n===== Budget Tracker =====\n"
        "1) Add expense\n"
        "2) Add income\n"
        "3) Add savings deposit\n"
        "4) View transactions\n"
        "5) View summary\n"
        "6) Delete transaction\n"
        "7) Exit\n"
    )
    actions = {
        "1": ("expense", "Expense"),
        "2": ("income", "Income"),
        "3": ("savings", "Savings deposit"),
    }
    try:
        while True:
            print(menu)
            choice = input("Choose an option (1-7): ").strip()
            if choice in actions:
                ttype, label = actions[choice]
                category = input("Category (e.g., food, rent, salary): ").strip()
                amount = prompt_float("Amount: ")
                note = input("Note (optional): ").strip()
                entry = tracker.add_transaction(ttype, category, amount, note)
                print(f"Added {label.lower()}: {fmt_money(entry['amount'])} in '{entry['category']}'.")
            elif choice == "4":
                print_transactions(tracker)
            elif choice == "5":
                print_summary(tracker)
            elif choice == "6":
                print_transactions(tracker)
                if tracker.list_transactions():
                    try:
                        idx = int(input("Transaction number to delete: ").strip()) - 1
                        removed = tracker.remove_transaction(idx)
                        print(f"Deleted: {removed['type']} {fmt_money(removed['amount'])} ({removed['category']}).")
                    except (ValueError, IndexError):
                        print("Invalid transaction number.")
            elif choice == "7":
                print("Goodbye! Your data is saved.")
                break
            else:
                print("Invalid option. Please choose 1-7.")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye! Your data is saved.")