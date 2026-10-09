import datetime

from storage import load_data, save_data
from tracker import BudgetTracker


def prompt_amount(msg):
    while True:
        try:
            value = float(input(msg))
        except ValueError:
            print("Enter a valid number.")
            continue
        if value > 0:
            return round(value, 2)
        print("Amount must be positive.")


def show_summary(tracker, month=None):
    totals = tracker.totals(month)
    label = f" ({month})" if month else " (all time)"
    print(f"\n--- Summary{label} ---")
    print(f"Income:     ${totals['income']:.2f}")
    print(f"Expenses:   ${totals['expense']:.2f}")
    print(f"Balance:    ${totals['balance']:.2f}")
    print(f"Savings:    ${totals['saving']:.2f}")
    print(f"Free funds: ${totals['net']:.2f}")
    cats = tracker.by_category("expense", month)
    if cats:
        print("Expenses by category:")
        for cat, amt in cats.items():
            print(f"  {cat}: ${amt:.2f}")


def main():
    tracker = BudgetTracker(load_data())
    menu = (
        "\n=== Budget Tracker ===\n"
        "1) Add expense\n"
        "2) Add income\n"
        "3) Add savings deposit\n"
        "4) View all transactions\n"
        "5) Monthly summary\n"
        "6) All-time summary\n"
        "7) Add savings goal\n"
        "8) Contribute to goal\n"
        "9) View goals\n"
        "0) Save & exit\n"
    )
    try:
        while True:
            print(menu)
            choice = input("Choose an option: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                category = input("Category: ").strip() or "General"
                note = input("Note (optional): ").strip()
                tracker.add_transaction("expense", prompt_amount("Amount: "), category, note)
                save_data(tracker.data)
                print("Expense recorded.")
            elif choice == "2":
                source = input("Source: ").strip() or "Income"
                tracker.add_transaction("income", prompt_amount("Amount: "), source)
                save_data(tracker.data)
                print("Income recorded.")
            elif choice == "3":
                tracker.add_transaction("saving", prompt_amount("Amount: "), "Savings")
                save_data(tracker.data)
                print("Savings deposit recorded.")
            elif choice == "4":
                entries = tracker.transactions()
                if not entries:
                    print("No transactions yet.")
                for t in entries:
                    print(f"{t['date']} [{t['type'].upper():7}] ${t['amount']:>9.2f}  {t['category']}  {t['note']}")
            elif choice == "5":
                month = input("Month (YYYY-MM, blank for current): ").strip()
                if not month:
                    month = datetime.date.today().strftime("%Y-%m")
                show_summary(tracker, month)
            elif choice == "6":
                show_summary(tracker)
            elif choice == "7":
                name = input("Goal name: ").strip()
                if not name:
                    print("Goal name required.")
                    continue
                tracker.add_goal(name, prompt_amount("Target amount: "))
                save_data(tracker.data)
                print("Goal created.")
            elif choice == "8":
                goals = tracker.data["goals"]
                if not goals:
                    print("No goals yet. Add one first.")
                    continue
                print("\n".join(tracker.goals_report()))
                idx = input("Goal number: ").strip()
                if not idx.isdigit() or int(idx) >= len(goals):
                    print("Invalid goal number.")
                    continue
                amount = prompt_amount("Contribution amount: ")
                goal, added = tracker.contribute_goal(int(idx), amount)
                if added <= 0:
                    print(f"'{goal['name']}' is already fully funded.")
                    continue
                tracker.add_transaction("saving", added, f"Goal: {goal['name']}")
                save_data(tracker.data)
                print(f"Added ${added:.2f} to '{goal['name']}'.")
            elif choice == "9":
                report = tracker.goals_report()
                print("\n".join(report) if report else "No goals yet.")
            else:
                print("Invalid option, try again.")
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        save_data(tracker.data)
        print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()