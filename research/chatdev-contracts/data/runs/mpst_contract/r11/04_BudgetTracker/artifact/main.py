from storage import load_data, save_data
from tracker import BudgetTracker


def fmt(x):
    return f"${x:,.2f}"


def read_amount(prompt):
    while True:
        try:
            v = float(input(prompt))
            if v > 0:
                return round(v, 2)
            print("Amount must be positive.")
        except ValueError:
            print("Enter a valid number.")


def read_int(prompt, limit):
    while True:
        try:
            v = int(input(prompt))
            if 0 <= v < limit:
                return v
        except ValueError:
            pass
        print(f"Enter a number between 0 and {limit - 1}.")


def show_transactions(tracker):
    txs = tracker.transactions()
    if not txs:
        print("No transactions recorded yet.")
        return
    print(f"{'#':>3} {'Date':<12} {'Type':<8} {'Category':<15} {'Amount':>12}  Note")
    print("-" * 70)
    for i, t in enumerate(txs):
        print(f"{i:>3} {t['date']:<12} {t['type']:<8} {t['category']:<15} "
              f"{fmt(t['amount']):>12}  {t['note']}")


def show_summary(tracker):
    income, expenses, balance = tracker.totals()
    print("\n--- Summary ---")
    print(f"Total income:   {fmt(income)}")
    print(f"Total expenses: {fmt(expenses)}")
    print(f"Savings:        {fmt(balance)}")
    cats = tracker.by_category()
    if cats:
        print("Expenses by category:")
        for c, a in sorted(cats.items(), key=lambda kv: -kv[1]):
            pct = (a / expenses * 100) if expenses else 0
            print(f"  {c:<15} {fmt(a):>12} ({pct:.1f}%)")


def show_goals(tracker):
    goals = tracker.goals()
    if not goals:
        print("No savings goals set.")
        return
    for i, g in enumerate(goals):
        pct = (g["saved"] / g["target"] * 100) if g["target"] else 0
        bar = "#" * int(pct // 5)
        print(f"[{i}] {g['name']}: {fmt(g['saved'])} / {fmt(g['target'])} "
              f"({pct:.0f}%) |{bar}")


def main():
    tracker = BudgetTracker(load_data())
    while True:
        print("\n=== Budget Tracker ===")
        print("1) Add expense      2) Add income        3) List transactions")
        print("4) Delete trans.    5) Summary           6) Add savings goal")
        print("7) Contribute goal  8) View goals        9) Save & exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            cat = input("Category (e.g. food, rent): ").strip() or "general"
            amt = read_amount("Amount: ")
            note = input("Note (optional): ").strip()
            tracker.add_transaction("expense", cat, amt, note)
            print("Expense added.")
        elif choice == "2":
            cat = input("Source (e.g. salary): ").strip() or "income"
            amt = read_amount("Amount: ")
            note = input("Note (optional): ").strip()
            tracker.add_transaction("income", cat, amt, note)
            print("Income added.")
        elif choice == "3":
            show_transactions(tracker)
        elif choice == "4":
            show_transactions(tracker)
            if tracker.transactions():
                idx = read_int("Index to delete: ", len(tracker.transactions()))
                removed = tracker.remove_transaction(idx)
                if removed:
                    print(f"Removed: {removed['type']} {fmt(removed['amount'])}")
                else:
                    print("Invalid index.")
        elif choice == "5":
            show_summary(tracker)
        elif choice == "6":
            name = input("Goal name: ").strip() or "Savings"
            target = read_amount("Target amount: ")
            tracker.add_goal(name, target)
            print("Goal added.")
        elif choice == "7":
            show_goals(tracker)
            if tracker.goals():
                idx = read_int("Goal index: ", len(tracker.goals()))
                amt = read_amount("Contribution amount: ")
                if tracker.contribute_goal(idx, amt):
                    print("Contribution recorded.")
                else:
                    print("Invalid goal index.")
        elif choice == "8":
            show_goals(tracker)
        elif choice == "9":
            save_data(tracker.data)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()