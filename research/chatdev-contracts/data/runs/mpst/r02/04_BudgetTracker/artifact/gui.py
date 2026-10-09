'''Tkinter GUI for the budget tracker application.'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from database import Database
import charts
DEFAULT_CATEGORIES = [
    "Food", "Rent", "Utilities", "Transport", "Entertainment",
    "Health", "Shopping", "Education", "Other",
]
class BudgetTrackerApp:
    """Main application window: summary bar plus four functional tabs."""
    def __init__(self, root: tk.Tk, db: Database) -> None:
        self.root = root
        self.db = db
        self.root.title("Budget Tracker")
        self.root.geometry("900x640")
        self.root.minsize(820, 560)
        self._selected_transaction_id = None  # id of transaction loaded into the form
        self._selected_goal_id = None         # id of the savings goal selected for deposit
        self._build_summary_bar()
        self._build_notebook()
        self._build_transactions_tab()
        self._build_budgets_tab()
        self._build_savings_tab()
        self._build_charts_tab()
        self._refresh_all()
    # ------------------------------------------------------------------ #
    # Widget construction
    # ------------------------------------------------------------------ #
    def _build_summary_bar(self) -> None:
        """Build the top bar showing this month's income/expenses/balance and total savings."""
        bar = tk.Frame(self.root, bd=1, relief="sunken")
        bar.pack(side=tk.TOP, fill=tk.X)
        self._lbl_income = tk.Label(bar, text="Income: 0.00", fg="#5cb85c")
        self._lbl_expenses = tk.Label(bar, text="Expenses: 0.00", fg="#d9534f")
        self._lbl_balance = tk.Label(bar, text="Balance: 0.00")
        self._lbl_savings = tk.Label(bar, text="Total Savings: 0.00", fg="#5bc0de")
        for label in (self._lbl_income, self._lbl_expenses,
                      self._lbl_balance, self._lbl_savings):
            label.pack(side=tk.LEFT, padx=14, pady=6)
    def _build_notebook(self) -> None:
        """Create the tab container."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    def _build_transactions_tab(self) -> None:
        """Build the Transactions tab: entry form plus table of all transactions."""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Transactions")
        form = tk.LabelFrame(tab, text="Add / Edit Transaction")
        form.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)
        tk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e", padx=4, pady=3)
        self._date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(form, textvariable=self._date_var, width=12).grid(row=0, column=1, padx=4, pady=3)
        tk.Label(form, text="Type:").grid(row=0, column=2, sticky="e", padx=4)
        self._type_var = tk.StringVar(value="expense")
        ttk.Combobox(form, textvariable=self._type_var, values=["expense", "income"],
                     state="readonly", width=10).grid(row=0, column=3, padx=4)
        tk.Label(form, text="Category:").grid(row=0, column=4, sticky="e", padx=4)
        self._category_var = tk.StringVar(value=DEFAULT_CATEGORIES[0])
        ttk.Combobox(form, textvariable=self._category_var, values=DEFAULT_CATEGORIES,
                     width=14).grid(row=0, column=5, padx=4)
        tk.Label(form, text="Amount:").grid(row=1, column=0, sticky="e", padx=4, pady=3)
        self._amount_var = tk.StringVar()
        tk.Entry(form, textvariable=self._amount_var, width=12).grid(row=1, column=1, padx=4)
        tk.Label(form, text="Description:").grid(row=1, column=2, sticky="e", padx=4)
        self._desc_var = tk.StringVar()
        tk.Entry(form, textvariable=self._desc_var, width=30).grid(
            row=1, column=3, columnspan=3, sticky="we", padx=4)
        buttons = tk.Frame(form)
        buttons.grid(row=2, column=0, columnspan=6, pady=6)
        tk.Button(buttons, text="Add", command=self._on_add_transaction).pack(side=tk.LEFT, padx=4)
        tk.Button(buttons, text="Update Selected", command=self._on_update_transaction).pack(side=tk.LEFT, padx=4)
        tk.Button(buttons, text="Delete Selected", command=self._on_delete_transaction).pack(side=tk.LEFT, padx=4)
        tk.Button(buttons, text="Clear Form", command=self._clear_transaction_form).pack(side=tk.LEFT, padx=4)
        table = tk.LabelFrame(tab, text="All Transactions")
        table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=6)
        columns = ("id", "date", "type", "category", "amount", "description")
        self._tx_tree = ttk.Treeview(table, columns=columns, show="headings", selectmode="browse")
        for col, width, anchor in (("id", 40, "center"), ("date", 95, "center"),
                                   ("type", 70, "center"), ("category", 110, "center"),
                                   ("amount", 95, "e"), ("description", 230, "w")):
            self._tx_tree.heading(col, text=col.capitalize())
            self._tx_tree.column(col, width=width, anchor=anchor)
        scrollbar = ttk.Scrollbar(table, orient=tk.VERTICAL, command=self._tx_tree.yview)
        self._tx_tree.configure(yscrollcommand=scrollbar.set)
        self._tx_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._tx_tree.bind("<<TreeviewSelect>>", self._on_transaction_select)