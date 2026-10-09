import math
from datetime import datetime
from tracker import BudgetTracker


def prompt_float(msg):
    while True:
        try:
            value = float(input(msg).strip())
            if value < 0 or not math.isfinite(value):
                print("Value must be a non-negative number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def parse_nonneg(raw):
    """Return a non-negative finite float parsed from raw, or None if invalid."""
    try:
        value = float(raw)
    except ValueError:
        return None
    if value < 0 or not math.isfinite(value):
        return None
    return value


def prompt_date():
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
    category = input("Category: ").strip() or "Uncategorized"
    description = input("Description: ").strip() or "-"
    amount = prompt_float("Amount: ")
    date = prompt_date()
    t = tracker.add_transaction(ttype, category, description, amount, date)
    sign = "+" if ttype == "income" else "-"
    print(f"Added {ttype}: {t.date} {t.category} {t.description} {sign}${t.amount:.2f}")


def show_transactions(tracker):
    if not tracker.transactions:
        print("No transactions recorded.")
        return
    for i, t in enumerate(tracker.transactions, 1):
        sign = "+" if t.ttype == "income" else "-"
        print(f"{i:3}. {t.date} [{t.ttype:7}] {t.category:15} {t.description:25} {sign}${t.amount:.2f}")


def remove_transaction(tracker):
    show_transactions(tracker)
    raw = input("Number to remove (blank to cancel): ").strip()
    if not raw:
        return
    try:
        index = int(raw) - 1
    except ValueError:
        print("Invalid number.")
        return
    removed = tracker.remove_transaction(index)
    print(f"Removed: {removed.date} {removed.description}" if removed else "Invalid index.")


def show_summary(tracker):
    month = input("Month (YYYY-MM, blank for all time): ").strip()
    if len(month) != 7:
        month = None
    income, expenses, savings = tracker.totals(month)
    print(f"\n=== Summary ({month or 'All time'}) ===")
    print(f"Income:   ${income:.2f}")
    print(f"Expenses: ${expenses:.2f}")
    print(f"Savings:  ${savings:.2f}")
    breakdown = tracker.category_breakdown(month)
    if breakdown:
        print("Expenses by category:")
        for cat, amt in sorted(breakdown.items(), key=lambda x: -x[1]):
            print(f"  {cat:15} ${amt:.2f}")


def show_monthly_report(tracker):
    raw = input("Month (YYYY-MM, blank for current): ").strip()
    month = raw if raw else datetime.now().strftime("%Y-%m")
    print()
    print(tracker.monthly_report(month))


def set_budget(tracker):
    raw = input(f"Monthly income goal (current {tracker.budget.monthly_income_goal:.2f}, blank=keep): ").strip()
    if raw:
        value = parse_nonneg(raw)
        if value is None:
            print("Invalid number; income goal unchanged.")
        else:
            tracker.set_budget(income_goal=value)
    raw = input(f"Monthly savings goal (current {tracker.budget.savings_goal:.2f}, blank=keep): ").strip()
    if raw:
        value = parse_nonneg(raw)
        if value is None:
            print("Invalid number; savings goal unchanged.")
        else:
            tracker.set_budget(savings_goal=value)
    raw = input("Category limits as 'food:300,rent:900' (blank=keep): ").strip()
    if raw:
        limits = {}
        for part in raw.split(","):
            if ":" in part:
                cat, amt = part.split(":", 1)
                value = parse_nonneg(amt.strip())
                if value is None:
                    print(f"Skipped invalid limit '{part}'.")
                else:
                    limits[cat.strip()] = value
        if limits:
            tracker.set_budget(category_limits=limits)
    print("Budget updated.")


MENU = """
=== Budget Tracker ===
1. Add expense
2. Add income
3. List transactions
4. Remove transaction
5. View summary
6. Monthly report
7. Set budget goals
8. Exit
"""


def main():
    tracker = BudgetTracker()
    print("Welcome to Budget Tracker! Data is saved to budget_data.json")
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction(tracker, "expense")
        elif choice == "2":
            add_transaction(tracker, "income")
        elif choice == "3":
            show_transactions(tracker)
        elif choice == "4":
            remove_transaction(tracker)
        elif choice == "5":
            show_summary(tracker)
        elif choice == "6":
            show_monthly_report(tracker)
        elif choice == "7":
            set_budget(tracker)
        elif choice == "8":
            print("Goodbye! All data saved.")
            break
        else:
            print("Invalid option, please choose 1-8.")


if __name__ == "__main__":
    main()