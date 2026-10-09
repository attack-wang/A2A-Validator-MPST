from tracker import BudgetTracker


def fmt(x):
    return f"${x:,.2f}"


def print_transactions(ts):
    if not ts:
        print("No transactions recorded.")
        return
    print(f"{'ID':>4} {'Date':<12} {'Type':<9} {'Category':<15} {'Description':<25} {'Amount':>12}")
    print("-" * 82)
    for t in ts:
        print(f"{t.id:>4} {t.date:<12} {t.kind:<9} {t.category:<15} {t.description[:24]:<25} {fmt(t.amount):>12}")


def prompt_float(msg):
    while True:
        try:
            v = float(input(msg).strip())
            if v <= 0:
                print("Amount must be positive.")
                continue
            return v
        except ValueError:
            print("Enter a valid number.")


def prompt_date():
    d = input("Date (YYYY-MM-DD, blank=today): ").strip()
    return d or None


def show_summary(tr):
    s = tr.summary()
    print("\n=== Overall Summary ===")
    print(f"Income:   {fmt(s['income'])}")
    print(f"Expenses: {fmt(s['expenses'])}")
    print(f"Savings:  {fmt(s['savings'])}")
    print(f"Available balance (income - expenses - savings): {fmt(s['balance'])}")


def main():
    tr = BudgetTracker()
    menu = (
        "\n=== Budget Tracker ===\n"
        "1) Add expense\n"
        "2) Add income\n"
        "3) Add savings deposit\n"
        "4) List transactions\n"
        "5) Delete transaction\n"
        "6) Overall summary\n"
        "7) Expense breakdown by category\n"
        "8) Monthly report\n"
        "9) Exit\n"
    )
    while True:
        print(menu)
        try:
            choice = input("Choose an option: ").strip()
            if choice == "1":
                t = tr.add("expense", input("Category: ").strip() or "General",
                           input("Description: ").strip(), prompt_float("Amount: "), prompt_date())
                print(f"Added expense #{t.id}.")
            elif choice == "2":
                t = tr.add("income", input("Source: ").strip() or "Income",
                           input("Description: ").strip(), prompt_float("Amount: "), prompt_date())
                print(f"Added income #{t.id}.")
            elif choice == "3":
                t = tr.add("savings", input("Goal/Category: ").strip() or "Savings",
                           input("Description: ").strip(), prompt_float("Amount: "), prompt_date())
                print(f"Added savings deposit #{t.id}.")
            elif choice == "4":
                print_transactions(tr.list_all())
            elif choice == "5":
                print_transactions(tr.list_all())
                tid = int(input("ID to delete: ").strip())
                tr.delete(tid)
                print(f"Deleted transaction #{tid}.")
            elif choice == "6":
                show_summary(tr)
            elif choice == "7":
                cats = tr.by_category("expense")
                if not cats:
                    print("No expenses recorded.")
                else:
                    total = sum(cats.values())
                    print("\n=== Expenses by Category ===")
                    for c, v in cats.items():
                        print(f"{c:<20} {fmt(v):>12} ({v / total * 100:.1f}%)")
            elif choice == "8":
                m = input("Month (YYYY-MM, blank=this month): ").strip() or None
                r = tr.monthly(m)
                print(f"\n=== Report for {r['month']} ===")
                print(f"Income: {fmt(r['income'])} | Expenses: {fmt(r['expenses'])} | "
                      f"Savings: {fmt(r['savings'])} | Net: {fmt(r['balance'])}")
            elif choice == "9":
                print("Goodbye! Data saved to budget_data.json")
                break
            else:
                print("Invalid option.")
        except EOFError:
            print("\nInput stream closed. Data saved to budget_data.json")
            break
        except KeyboardInterrupt:
            print("\nInterrupted. Data saved.")
            break
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()