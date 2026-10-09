"""Budget Tracker - monitor expenses and savings."""
import math
from datetime import datetime
from storage import Storage
from tracker import BudgetTracker


def money(x):
    return f"${x:,.2f}"


def ask(prompt, cast=str, default=None):
    raw = input(prompt).strip()
    if not raw:
        return default if default is not None else cast("")
    return cast(raw)


def read_amount(prompt="Amount: "):
    while True:
        try:
            amount = float(ask(prompt))
            if not math.isfinite(amount) or amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print("Enter a positive finite number.")


def add_tx(tracker, kind):
    hint = "e.g. food, rent, travel" if kind == "expense" else "e.g. salary, gift"
    category = ask(f"Category ({hint}): ") or "General"
    description = ask("Description: ") or "-"
    amount = read_amount()
    date = ask("Date (YYYY-MM-DD, blank=today): ", default=datetime.now().strftime("%Y-%m-%d"))
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return
    t = tracker.add_transaction(kind, category, description, amount, date)
    print(f"Recorded {kind}: {t.category} {money(t.amount)} on {t.date}")


def list_tx(tracker):
    if not tracker.transactions:
        print("No transactions yet.")
        return
    print(f"{'ID':<9}{'Date':<12}{'Type':<9}{'Category':<15}{'Description':<25}{'Amount':>12}")
    for t in reversed(tracker.transactions):
        print(f"{t.id:<9}{t.date:<12}{t.kind:<9}{t.category:<15}{t.description:<25}{money(t.amount):>12}")


def monthly(tracker):
    try:
        year = ask("Year (blank=current): ", cast=int, default=datetime.now().year)
        month = ask("Month 1-12 (blank=current): ", cast=int, default=datetime.now().month)
        if not 1 <= month <= 12:
            raise ValueError
    except ValueError:
        print("Invalid date.")
        return
    rows, inc, exp, net = tracker.monthly_summary(year, month)
    print(f"\nSummary {year}-{month:02d}: income {money(inc)}, expenses {money(exp)}, "
          f"net {money(net)} ({len(rows)} transactions)")


def breakdown(tracker):
    cats = tracker.category_breakdown()
    if not cats:
        print("No expenses recorded.")
        return
    total = sum(cats.values())
    print(f"{'Category':<15}{'Amount':>12}{'Share':>8}")
    for cat, amt in cats.items():
        print(f"{cat:<15}{money(amt):>12}{amt / total * 100:>7.1f}%")


def add_goal(tracker):
    name = ask("Goal name: ") or "Savings"
    try:
        target = float(ask("Target amount: "))
        if not math.isfinite(target) or target <= 0:
            raise ValueError
    except ValueError:
        print("Invalid target.")
        return
    tracker.add_goal(name, target)
    print(f"Goal '{name}' created with target {money(target)}.")


def show_goals(tracker):
    if not tracker.goals:
        print("No savings goals yet.")
        return
    for g in tracker.goals:
        bar = "#" * int(g.progress // 5)
        print(f"{g.name}: {money(g.saved)} / {money(g.target)} [{bar:<20}] {g.progress:.0f}%")


def contribute(tracker):
    if not tracker.goals:
        print("Create a goal first.")
        return
    name = ask("Goal name: ")
    amount = read_amount("Amount to add: ")
    g = tracker.contribute(name, amount)
    print(f"{g.name}: {money(g.saved)} / {money(g.target)} ({g.progress:.0f}%)" if g else "Goal not found.")


def balance(tracker):
    print(f"Balance: {money(tracker.balance())} "
          f"(income {money(tracker.total_income())}, expenses {money(tracker.total_expenses())})")


MENU = {
    "1": ("Add expense", lambda t: add_tx(t, "expense")),
    "2": ("Add income", lambda t: add_tx(t, "income")),
    "3": ("List transactions", list_tx),
    "4": ("Monthly summary", monthly),
    "5": ("Category breakdown", breakdown),
    "6": ("Add savings goal", add_goal),
    "7": ("Contribute to goal", contribute),
    "8": ("View savings goals", show_goals),
    "9": ("Overall balance", balance),
}


def main():
    storage = Storage("budget_data.json")
    tracker = storage.load()
    print("Welcome to Budget Tracker! (data file: budget_data.json)")
    while True:
        print("\n=== Budget Tracker ===")
        for key in sorted(MENU):
            print(f"{key}) {MENU[key][0]}")
        print("0) Save & exit")
        try:
            choice = input("Choose: ").strip()
        except (EOFError, KeyboardInterrupt):
            storage.save(tracker)
            print("\nInput ended. Saved. Goodbye!")
            break
        if choice == "0":
            storage.save(tracker)
            print("Saved. Goodbye!")
            break
        action = MENU.get(choice)
        if not action:
            print("Invalid choice.")
            continue
        try:
            action[1](tracker)
        except (EOFError, KeyboardInterrupt):
            storage.save(tracker)
            print("\nInput ended. Saved. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()