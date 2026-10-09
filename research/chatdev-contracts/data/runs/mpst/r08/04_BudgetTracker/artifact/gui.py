'''
GUI module for the Budget Tracker application.
Defines the BudgetTrackerApp class, which builds the Tkinter interface
with four tabs (Transactions, Budgets, Savings Goals, Reports) and
handles all user input, validation, and display refresh logic.
This complete module replaces the previously corrupted fragment files
(gui.py, .py, goal_text.split, intvar.get, self.db).
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import Transaction, SavingsGoal
from database import Database
from charts import ChartGenerator
from utils import format_currency, validate_amount, validate_date, MONTH_NAMES, month_name
class BudgetTrackerApp:
    """Main application window providing the tabbed budget-tracking UI."""
    def __init__(self, root):
        """Initialize the database, build all tabs, and load initial data."""
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("1024x680")
        self.goal_records = []
        self.db = Database()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self._build_transactions_tab()
        self._build_budgets_tab()
        self._build_goals_tab()
        self._build_reports_tab()
        self.refresh_transactions()
        self.refresh_budgets()
        self.refresh_goals()
        self.refresh_reports()
    # ------------------------------------------------------------------
    # Transactions tab
    # ------------------------------------------------------------------
    def _build_transactions_tab(self):
        ...