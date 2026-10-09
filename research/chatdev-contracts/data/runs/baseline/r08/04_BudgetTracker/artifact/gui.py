'''
gui.py
Main window of the Budget Tracker application.
Builds a tabbed interface (Dashboard, Transactions, Savings Goals) on top
of the models/storage layers and refreshes all views after every change.
'''
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from models import Budget, Transaction, SavingsGoal
from storage import JSONStorage
from charts import PieChart, LineChart, BarChart
from dialogs import TransactionDialog, GoalDialog, ContributionDialog
CURRENCY = "${:,.2f}"
class BudgetTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ChatDev Budget Tracker")
        self.geometry("1000x680")
        self.minsize(900, 600)
        self.storage = JSONStorage()
        txns, goals = self.storage.load()
        self.budget = Budget(
            transactions=[Transaction.from_dict(d) for d in txns],
            goals=[SavingsGoal.from_dict(g) for g in goals],
        )
        self._build_menu()
        self._build_notebook()
        self.refresh_all()
        self.protocol("WM_DELETE_WINDOW", self._on_close)