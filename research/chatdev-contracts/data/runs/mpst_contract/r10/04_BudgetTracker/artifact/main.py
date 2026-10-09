"""Budget Tracker CLI - monitor expenses and savings."""
import math
import sys

from budget import BudgetManager


def prompt_float(msg):
    while True:
        try:
            value = float(input(msg).strip().replace("$", ""))
            if not math.isfinite(value) or value <= 0:
                print("Amount must be a positive finite number.")
                continue
            return round(value, 2)
        except ValueError:
            print("Please enter a valid number.")


def prompt_nonempty(msg):
    while True:
        value = input(msg).strip()
        if value:
            return value
        print("Value cannot be empty.")


def add_transaction(mgr, ttype):
    label = "income" if ttype == "income" else "expense"
    category = prompt_nonempty(f"Category for {label} (e.g. salary, food): ")
    amount = prompt_float("Amount: ")
    note = input("Note (optional): ").strip()
    t = mgr.add_transaction(ttype, category, amount, note)
    print(f"Recorded {label} {t.id}: {category} ${t.amount:,.2f}")


def add_goal(mgr):
    name = prompt_nonempty("Goal name: ")
    target = prompt_float("Target amount: ")
    try:
        g = mgr.add_goal(name, target)
        print(f"Goal '{g.name}' created with target ${g.target:,.2f}.")
    except ValueError as e:
        print(f"Error: {e}")


def contribute_goal(mgr):
    if not mgr.goals:
        print("No savings goals yet. Add one first.")
        return
    print("Goals: " + ", ".join(g.name for g in mgr.goals))
    name = prompt_nonempty("Goal to fund: ")
    amount = prompt_float("Amount to add: ")
    try:
        g = mgr.contribute(name, amount)
        print(f"'{g.name}' now at ${g.saved:,.2f} of ${g.target:,.2f} ({g.progress:.1f}%).")
    except ValueError as e:
        print(f"Error: {e}")


def delete_transaction(mgr):
    print(mgr.list_transactions())
    tid = input("Transaction ID to delete (blank to cancel): ").strip()
    if tid and mgr.delete_transaction(tid):
        print("Deleted.")
    elif tid:
        print("ID not found.")


MENU = """
========= Budget Tracker =========
1) Add income
2) Add expense
3) List transactions
4) Delete transaction
5) Add savings goal
6) Contribute to savings goal
7) View summary
8) Exit
=================================="""


def main():
    mgr = BudgetManager()
    print("Welcome to Budget Tracker! Data is saved to budget_data.json.")
    actions = {"1": lambda: add_transaction(mgr, "income"),
               "2": lambda: add_transaction(mgr, "expense"),
               "3": lambda: print(mgr.list_transactions()),
               "4": lambda: delete_transaction(mgr),
               "5": add_goal,
               "6": contribute_goal,
               "7": lambda: print(mgr.summary())}
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "8":
            print("Goodbye! Your budget data has been saved.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option, please choose 1-8.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Data saved.")
        sys.exit(0)