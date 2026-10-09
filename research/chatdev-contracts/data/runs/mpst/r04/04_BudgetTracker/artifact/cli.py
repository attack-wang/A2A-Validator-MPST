'''
cli.py
Interactive command-line interface for the Budget Tracker. Provides
menus for managing transactions, budgets, savings goals, reports,
and charts.
'''
from datetime import datetime
from transaction import Transaction
from tracker import BudgetTracker
from reports import ReportGenerator
from visualizer import Visualizer
class BudgetTrackerCLI:
    """Text-based user interface driving the BudgetTracker."""
    def __init__(self, filepath="budget_data.json"):
        self.tracker = BudgetTracker(filepath)
        self.reports = ReportGenerator(self.tracker)
        self.visualizer = Visualizer(self.tracker)
    def run(self):
        self.print_welcome()
        while True:
            self.print_main_menu()
            choice = input("Select an option: ").strip()
            if choice == "1":
                self.handle_add_transaction()
            elif choice == "2":
                self.handle_view_transactions()
            elif choice == "3":
                self.handle_budgets()
            elif choice == "4":
                self.handle_savings_goals()
            elif choice == "5":
                self.handle_reports()
            elif choice == "6":
                self.handle_charts()
            elif choice == "7" or choice.lower() in ("q", "quit", "exit"):
                print("Goodbye! Your data has been saved.")
                break
            else:
                print("Invalid option, please try again.\n")
    ...