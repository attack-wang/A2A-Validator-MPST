'''
gui.py
Graphical user interface for the budget tracker application.
BudgetTrackerGUI builds a Tkinter window with four tabs:
  * Expenses - add, edit and delete expense records
  * Savings  - manage savings goals and track progress toward targets
  * Summary  - key figures such as totals and a category breakdown
  * Charts   - a pie chart of spending by category and a bar chart of
               monthly spending, drawn with native Tkinter canvases
The GUI talks to the BudgetManager for all data operations, so no
business logic lives in this module. Every tree view uses the record's
unique id as the Treeview item id, which guarantees that selection
handlers always retrieve the correct record.
'''
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from budget_manager import BudgetManager
# Fixed palette used for chart slices so colors remain consistent
CHART_COLORS = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC",
]
DEFAULT_CATEGORIES = [
    "Food", "Transport", "Housing", "Utilities", "Entertainment",
    "Health", "Shopping", "Education", "Other",
]
class BudgetTrackerGUI:
    """Main application window of the budget tracker."""
    def __init__(self, root, manager=None):
        self.root = root
        self.manager = manager if manager is not None else BudgetManager()
        self.selected_expense_id = None
        self.selected_goal_id = None
        self.root.title("Budget Tracker")
        self.root.geometry("960x660")
        self.root.minsize(860, 580)
        self._build_style()
        self._build_layout()
        self.refresh_all()
    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    def _build_style(self):
        """Configure the ttk theme and widget styles."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass  # Fall back to the default theme
        style.configure("Treeview", rowheight=24, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("TButton", padding=4)
    def _build_layout(self):
        """Create the tabbed notebook that hosts all four views."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.expenses_tab = ttk.Frame(self.notebook)
        self.savings_tab = ttk.Frame(self.notebook)
        self.summary_tab = ttk.Frame(self.notebook)
        self.charts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.expenses_tab, text="Expenses")
        self.notebook.add(self.savings_tab, text="Savings")
        self.notebook.add(self.summary_tab, text="Summary")
        self.notebook.add(self.charts_tab, text="Charts")
        self._setup_expenses_tab()
        self._setup_savings_tab()
        self._setup_summary_tab()
        self._setup_charts_tab()
    # ------------------------------------------------------------------
    # Expenses tab
    # ------------------------------------------------------------------
    def _setup_expenses_tab(self):
        """Build the expense entry form and the expense list view."""
        form = ttk.LabelFrame(self.expenses_tab, text="Expense details")
        form.pack(fill=tk.X, padx=10, pady=(10, 5))
        ttk.Label(form, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.amount_var, width=12).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(form, text="Category:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form, textvariable=self.category_var,
                                           values=DEFAULT_CATEGORIES, width=15)
        self.category_combo.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=4, sticky="e", padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form, textvariable=self.date_var, width=12).grid(row=0, column=5, sticky="w", padx=5, pady=5)
        ttk.Label(form, text="Description:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.description_var, width=40).grid(
            row=1, column=1, columnspan=3, sticky="w", padx=5, pady=5)
        buttons = ttk.Frame(form)
        buttons.grid(row=1, column=4, columnspan=2, sticky="w", padx=5, pady=5)
        ttk.Button(buttons, text="Add Expense", command=self.on_add_expense).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons, text="Update Selected", command=self.on_update_expense).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons, text="Delete Selected", command=self.on_delete_expense).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons, text="Clear Form", command=self.clear_expense_form).pack(side=tk.LEFT, padx=2)
        list_frame = ttk.LabelFrame(self.expenses_tab, text="Recorded expenses")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("date", "category", "description", "amount")
        self.expense_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.expense_tree.heading("date", text="Date")
        self.expense_tree.heading("category", text="Category")
        self.expense_tree.heading("description", text="Description")
        self.expense_tree.heading("amount", text="Amount")
        self.expense_tree.column("date", width=110, anchor="center")
        self.expense_tree.column("category", width=130, anchor="w")
        self.expense_tree.column("description", width=380, anchor="w")
        self.expense_tree.column("amount", width=110, anchor="e")
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)
        self.expense_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.expense_tree.bind("<<TreeviewSelect>>", self.on_expense_select)
        self.expense_total_var = tk.StringVar(value="Total expenses: 0.00")
        ttk.Label(self.expenses_tab, textvariable=self.expense_total_var,
                  font=("Helvetica", 11, "bold")).pack(anchor="e", padx=12, pady=(0, 8))
    def on_add_expense(self):
        """Validate the form and store a new expense record."""
        amount = self._parse_amount(self.amount_var.get())
        if amount is None:
            return
        category = self.category_var.get().strip()
        if not category:
            messagebox.showwarning("Missing category", "Please choose or type a category.")
            return
        date = self._parse_date(self.date_var.get())
        if date is None:
            return
        if not self._run_persist(self.manager.add_expense, amount=amount, category=category,
                                 description=self.description_var.get().strip(), date=date):
            return
        self.clear_expense_form()
        self.refresh_all()
    ...