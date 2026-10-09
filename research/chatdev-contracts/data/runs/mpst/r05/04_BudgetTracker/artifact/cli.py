'''
cli.py
Interactive command-line interface for the Budget Tracker.
BudgetCLI renders a menu-driven console UI on top of BudgetTracker
and ReportGenerator. All user input is validated by dedicated helper
methods so invalid values never reach the business layer.
'''
from datetime import date
from models import TRANSACTION_TYPES
class BudgetCLI:
    """Interactive menu-driven interface for the Budget Tracker."""
    def __init__(self, tracker, reports):
        self.tracker = tracker
        self.reports = reports
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Run the interactive main menu loop until the user quits."""
        print("\n" + "=" * 46)
        print("       WELCOME TO THE BUDGET TRACKER")
        print("=" * 46)
        while True:
            try:
                choice = self._main_menu()
                if choice == "1":
                    self._add_transaction("income")
                elif choice == "2":
                    self._add_transaction("expense")
                elif choice == "3":
                    self._add_transaction("savings")
                elif choice == "4":
                    self._list_transactions()
                elif choice == "5":
                    self._edit_transaction()
                elif choice == "6":
                    self._delete_transaction()
                elif choice == "7":
                    print("\n" + self.reports.full_report())
                elif choice == "8":
                    self._manage_goals()
                elif choice == "9":
                    self._manage_budgets()
                elif choice == "10":
                    self._export_csv()
                elif choice.strip().lower() in ("0", "q", "quit", "exit"):
                    print("\nSaving and exiting... goodbye!")
                    self.tracker.save()
                    break
                else:
                    print("Invalid choice — please enter a number from the menu.")
            except (KeyboardInterrupt, EOFError):
                print("\nSaving and exiting... goodbye!")
                self.tracker.save()
                break
    def _main_menu(self):
        """Print the main menu and return the user's (stripped) choice."""
        print("\n---------- MAIN MENU ----------")
        print(" 1. Add income")
        print(" 2. Add expense")
        print(" 3. Add savings deposit")
        print(" 4. List all transactions")
        print(" 5. Edit a transaction")
        print(" 6. Delete a transaction")
        print(" 7. View full report")
        print(" 8. Manage savings goals")
        print(" 9. Manage category budgets")
        print(" 10. Export transactions to CSV")
        print(" 0. Quit")
        return input("Select an option: ").strip()