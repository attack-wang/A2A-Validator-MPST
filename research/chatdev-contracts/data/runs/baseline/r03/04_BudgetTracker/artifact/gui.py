'''
gui.py
Tkinter graphical user interface for the Budget Tracker application.
The window is a tabbed notebook with five tabs:
    Dashboard    -- headline totals, savings-rate card, overall goal
                    progress and the most recent transactions.
    Transactions -- add, browse and delete income/expense records.
    Budgets      -- set monthly spending limits per category and see
                    how much of each budget has been used this month.
    Savings      -- create savings goals, contribute money to them and
                    track completion progress.
    Charts       -- a pie chart of spending by category and a bar chart
                    comparing monthly income and expenses.
All data mutations go through storage.DataManager, which persists to JSON.
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import calendar
import analytics
from models import Transaction, SavingsGoal
from storage import DataManager
EXPENSE_CATEGORIES = [
    "Food", "Rent & Utilities", "Transport", "Shopping",
    "Entertainment", "Health", "Education", "Travel", "Other",
]
INCOME_CATEGORIES = [
    "Salary", "Freelance", "Investments", "Gifts", "Other",
]
PIE_COLORS = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
              "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]
INCOME_BAR_COLOR = "#59a14f"
EXPENSE_BAR_COLOR = "#e15759"
OVER_BUDGET_COLOR = "#e15759"
UNDER_BUDGET_COLOR = "#59a14f"
def fmt_money(value):
    """Format a number as a currency string, e.g. -12.5 -> '-$12.50'."""
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"
def fmt_month(month_str):
    """'2024-05' -> 'May 2024' (falls back to the raw string)."""
    try:
        dt = datetime.strptime(month_str, "%Y-%m")
        return dt.strftime("%b %Y")
    except (ValueError, TypeError):
        return str(month_str)
class BudgetTrackerApp(tk.Tk):
    """Main application window: a notebook with five tabs."""
    def __init__(self):
        super().__init__()
        self.title("Budget Tracker — Expenses & Savings")
        self.geometry("1000x660")
        self.minsize(900, 600)
        self.data = DataManager()
        self._setup_style()
        self._build_ui()
        self.refresh_all()
    # ------------------------------------------------------------------
    # Appearance
    # ------------------------------------------------------------------
    def _setup_style(self):
        style = ttk.Style(self)
        for theme in ("vista", "aqua", "clam"):
            if theme in style.theme_names():
                style.theme_use(theme)
                break
        style.configure("TNotebook.Tab", padding=(14, 6))
        style.configure("CardValue.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("CardTitle.TLabel", font=("Segoe UI", 9))
        style.configure("Success.TButton", foreground=INCOME_BAR_COLOR)
        style.configure("Danger.TButton", foreground=EXPENSE_BAR_COLOR)
        self.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))
    # ------------------------------------------------------------------
    # Layout construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self._build_dashboard_tab()
        self._build_transactions_tab()
        self._build_budgets_tab()
        self._build_savings_tab()
        self._build_charts_tab()
    def _build_dashboard_tab(self):
        ... (fragment)
    def _build_transactions_tab(self):
        ...
    def _build_budgets_tab(self):
        ...
    def _build_savings_tab(self):
        ...
    def _build_charts_tab(self):
        ...
    # refresh methods, handlers, drawing...