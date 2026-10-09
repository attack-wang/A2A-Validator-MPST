'''
gui.py
Graphical user interface layer for the Budget Tracker application.
...
'''
import calendar
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from models import TransactionType
from budget_manager import BudgetManager
import charts
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    CHARTS_EMBEDDABLE = charts.MATPLOTLIB_AVAILABLE
except Exception:
    CHARTS_EMBEDDABLE = False
CURRENCY = "$"
TRANSACTION_FILTERS = [
    "All transactions", "This month", "Last month",
    "Expenses only", "Income only",
]
def _fmt_money(value):
    """Format a number as a currency string, e.g. $1,234.56."""
    return f"{CURRENCY}{value:,.2f}"
class BudgetTrackerGUI:
    """Main application window for the Budget Tracker."""
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self._chart_canvases = []
        self._setup_window()
        self._build_notebook()
        self.refresh_all()
    # ------------------------------------------------------------------
    # window scaffolding
    # ------------------------------------------------------------------
    def _setup_window(self):
        self.root.title("Budget Tracker – Expenses & Savings")
        self.root.geometry("900x640")
        self.root.minsize(820, 560)
        self.status_var = tk.StringVar(value="Ready.")
        self._build_status_bar()
    def _build_status_bar(self):
        bar = ttk.Frame(self.root, padding=(8, 4))
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(bar, textvariable=self.status_var, anchor="w").pack(fill=tk.X)
    def _set_status(self, message):
        self.status_var.set(message)
    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._build_dashboard_tab()
        self._build_add_tab()
        self._build_transactions_tab()
        if CHARTS_EMBEDDABLE:
            self._build_charts_tab()
        self._build_budget_tab()
    # ------------------------------------------------------------------
    # dashboard tab
    # ------------------------------------------------------------------
    def _build_dashboard_tab(self):
        tab = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(tab, text="Dashboard")
        selector = ttk.Frame(tab)
        selector.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(selector, text="Year:").pack(side=tk.LEFT)
        self.dash_year_var = tk.StringVar(value=str(datetime.now().year))
        self.dash_year_combo = ttk.Combobox(
            selector, textvariable=self.dash_year_var, state="readonly", width=10)
        self.dash_year_combo.pack(side=tk.LEFT, padx=(4, 16))
        self.dash_year_combo.bind("<<ComboboxSelected>>",
                                  lambda event: self._refresh_dashboard())
        ttk.Label(selector, text="Month:").pack(side=tk.LEFT)
        self.dash_month_var = tk.StringVar(
            value=calendar.month_name[datetime.now().month])
        self.dash_month_combo = ttk.Combobox(
            selector, textvariable=self.dash_month_var, state="readonly", width=12,
            values=["All months"] + [calendar.month_name[m] for m in range(1, 13)])
        self.dash_month_combo.pack(side=tk.LEFT, padx=4)
        self.dash_month_combo.bind("<<ComboboxSelected>>",
                                   lambda event: self._refresh_dashboard())
        cards = ttk.Frame(tab)
        cards.pack(fill=tk.X)
        self.income_card = self._make_card(cards, "Total Income", "#2e7d32")
        self.expense_card = self._make_card(cards, "Total Expenses", "#c62828")
        self.savings_card = self._make_card(cards, "Net Savings", "#1565c0")
        self.rate_card = self._make_card(cards, "Savings Rate", "#6a1b9a")
        progress = ttk.LabelFrame(tab, text="Monthly Budget Progress", padding=10)
        progress.pack(fill=tk.X, pady=12)
        self.budget_progress = ttk.Progressbar(progress, maximum=100.0)
        self.budget_progress.pack(fill=tk.X)
        self.budget_label_var = tk.StringVar(value="No budget goal set.")
        ttk.Label(progress, textvariable=self.budget_label_var).pack(
            anchor="w", pady=(4, 0))
        breakdown = ttk.LabelFrame(tab, text="Expenses by Category", padding=10)
        breakdown.pack(fill=tk.BOTH, expand=True)
        self.cat_tree = ttk.Treeview(
            breakdown, columns=("category", "amount"), show="headings", height=8)
        self.cat_tree.heading("category", text="Category")
        self.cat_tree.heading("amount", text="Total")
        self.cat_tree.column("category", anchor="w")
        self.cat_tree.column("amount", anchor="e", width=120, stretch=False)
        self.cat_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(breakdown, command=self.cat_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cat_tree.configure(yscrollcommand=scrollbar.set)
    def _make_card(self, parent, title, color):
        """Build one summary card and return its value StringVar."""
        card = ttk.Frame(parent, relief="solid", borderwidth=1, padding=10)
        card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6, pady=2)
        ttk.Label(card, text=title, foreground=color,
                  font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        value_var = tk.StringVar(value=_fmt_money(0))
        ttk.Label(card, textvariable=value_var,
                  font=("TkDefaultFont", 15, "bold")).pack(anchor="w", pady=(4, 0))
        return value_var
    def _dashboard_period(self):
        """Read the dashboard year/month selectors; (None, None) = all time."""
        year_text = self.dash_year_var.get()
        month_name = self.dash_month_var.get()
        year = None
        if year_text not in ("", "All years"):
            try:
                year = int(year_text)
            except ValueError:
                year = None
        month = None
        if year is not None and month_name in calendar.month_name:
            month = list(calendar.month_name).index(month_name)
        return year, month
    def _refresh_dashboard(self):
        year, month = self._dashboard_period()
        income = self.manager.total_income(year, month)
        expenses = self.manager.total_expenses(year, month)
        savings = self.manager.savings(year, month)
        rate = self.manager.savings_rate(year, month)
        self.income_card.set(_fmt_money(income))
        self.expense_card.set(_fmt_money(expenses))
        self.savings_card.set(_fmt_money(savings))
        self.rate_card.set(f"{rate:.1f}%")
        spent, budget, remaining, over_budget = self.manager.budget_status(year, month)
        if budget > 0:
            percent = min(spent / budget * 100.0, 100.0)
            self.budget_progress["value"] = percent
            if over_budget:
                self.budget_label_var.set(
                    f"Over budget by {_fmt_money(abs(remaining))} "
                    f"({_fmt_money(spent)} spent of {_fmt_money(budget)})")
            else:
                self.budget_label_var.set(
                    f"{_fmt_money(remaining)} remaining of {_fmt_money(budget)} "
                    f"({_fmt_money(spent)} spent)")
        else:
            self.budget_progress["value"] = 0
            self.budget_label_var.set(
                "No budget goal set. Set one in the Budget tab.")
        self.cat_tree.delete(*self.cat_tree.get_children())
        for category, total in self.manager.expenses_by_category(year, month).items():
            self.cat_tree.insert("", tk.END, values=(category, _fmt_money(total)))
        self._set_status("Dashboard updated.")