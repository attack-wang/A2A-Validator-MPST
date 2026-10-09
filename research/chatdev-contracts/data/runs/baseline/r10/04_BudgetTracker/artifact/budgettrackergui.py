import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from visualizer import Visualizer, MATPLOTLIB_AVAILABLE
if MATPLOTLIB_AVAILABLE:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
CATEGORIES = [...]
class BudgetTrackerGUI:
    def __init__(self, root, tracker):
        self.root = root
        self.tracker = tracker
        self.visualizer = Visualizer(tracker)
        root.title("Budget Tracker")
        root.geometry("900x650")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.expenses_frame = ttk.Frame(self.notebook)
        self.savings_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.expenses_frame, text="Expenses")
        self.notebook.add(self.savings_frame, text="Savings Goals")
        self.notebook.add(self.reports_frame, text="Reports")
        self._build_expenses_tab()
        self._build_savings_tab()
        self._build_reports_tab()
        self.refresh_all()