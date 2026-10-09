'''
main.py
Entry point for the Budget Tracker application. Wires together the
tracker (business logic), reports, and visualizer, then runs the
interactive main menu loop until the user chooses to exit.
'''
from tracker import BudgetTracker
from reports import ReportGenerator
from visualizer import Visualizer
from ui import (handle_add_transaction, handle_view_transactions,
                handle_edit_transaction, handle_delete_transaction,
                handle_set_budget, handle_budget_status,
                handle_savings_menu, handle_reports_menu,
                handle_visualizations)
def print_main_menu():
    """Print the top-level menu options."""
    print("\n================ BUDGET TRACKER ================")
    print("  1. Add transaction")
    print("  2. View transactions")
    print("  3. Edit transaction")
    print("  4. Delete transaction")
    print("  5. Set monthly budget")
    print("  6. Budget status")
    print("  7. Savings goals menu")
    print("  8. Reports menu")
    print("  9. Visualizations menu")
    print("  0. Exit")
    print("================================================")
def main():
    """Run the interactive Budget Tracker menu loop."""
    tracker = BudgetTracker()
    reports = ReportGenerator(tracker)
    viz = Visualizer()
    print("Welcome to Budget Tracker!")
    reports.overall_summary()
    try:
        while True:
            print_main_menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                handle_add_transaction(tracker)
            elif choice == "2":
                handle_view_transactions(tracker)
            elif choice == "3":
                handle_edit_transaction(tracker)
            elif choice == "4":
                handle_delete_transaction(tracker)
            elif choice == "5":
                handle_set_budget(tracker)
            elif choice == "6":
                handle_budget_status(tracker, reports)
            elif choice == "7":
                handle_savings_menu(tracker, reports)
            elif choice == "8":
                handle_reports_menu(tracker, reports, viz)
            elif choice == "9":
                handle_visualizations(tracker, viz)
            elif choice == "0":
                print("Data saved. Goodbye!")
                break
            else:
                print("Invalid option, please try again.")
    finally:
        # Always persist on the way out, even after Ctrl+C / unexpected exits.
        tracker.save()
if __name__ == "__main__":
    main()