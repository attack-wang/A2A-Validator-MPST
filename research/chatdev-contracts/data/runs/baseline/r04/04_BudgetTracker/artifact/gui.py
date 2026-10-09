'''
gui.py
Tkinter-based graphical user interface for the Budget Tracker application.
Classes:
    BudgetTrackerApp: Main application window providing tabs for managing
        transactions, viewing dashboard charts, setting budgets, and
        reviewing monthly reports.
'''
import calendar
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models import Transaction, Category
from tracker import BudgetTracker
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from visualizations import ChartGenerator
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
class BudgetTrackerApp:
    """Main application window for the Budget Tracker."""
    def __init__(self, root):
        self.root = root
        self.tracker = BudgetTracker()
        self.selected_transaction_id = None
        self._configure_window()
        self._build_notebook()
        self._build_transactions_tab()
        self._build_dashboard_tab()
        self._build_budget_tab()
        self._build_reports_tab()
        self.refresh_all()
    # ------------------------------------------------------------------ #
    # Window / layout skeleton
    # ------------------------------------------------------------------ #
    def _configure_window(self):
        """Set up the main window title and default size."""
        self.root.title("Budget Tracker")
        self.root.geometry("1000x680")
        self.root.minsize(880, 600)
    def _build_notebook(self):
        """Create the tabbed notebook and the four main tab frames."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.transactions_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.budget_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.transactions_frame, text="Transactions")
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.budget_frame, text="Budgets")
        self.notebook.add(self.reports_frame, text="Reports")
    # ------------------------------------------------------------------ #
    # Transactions tab
    # ------------------------------------------------------------------ #
    def _build_transactions_tab(self):
        """Build the transaction entry form and the transaction list."""
        form = ttk.LabelFrame(self.transactions_frame, text="Add / Edit Transaction")
        form.pack(fill=tk.X, padx=8, pady=8)
        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)
        self.date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ttk.Entry(form, textvariable=self.date_var, width=12).grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(form, text="Description:").grid(row=0, column=2, sticky=tk.W, padx=6, pady=4)
        self.description_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.description_var, width=24).grid(row=0, column=3, padx=6, pady=4)
        ttk.Label(form, text="Amount:").grid(row=1, column=0, sticky=tk.W, padx=6, pady=4)
        self.amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.amount_var, width=12).grid(row=1, column=1, padx=6, pady=4)
        ttk.Label(form, text="Type:").grid(row=1, column=2, sticky=tk.W, padx=6, pady=4)
        self.type_var = tk.StringVar(value=Transaction.EXPENSE)
        type_combo = ttk.Combobox(form, textvariable=self.type_var,
                                  values=[Transaction.EXPENSE, Transaction.INCOME],
                                  state="readonly", width=10)
        type_combo.grid(row=1, column=3, sticky=tk.W, padx=6, pady=4)
        type_combo.bind("<<ComboboxSelected>>", self._on_type_changed)
        ttk.Label(form, text="Category:").grid(row=2, column=0, sticky=tk.W, padx=6, pady=4)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form, textvariable=self.category_var,
                                           values=Category.get_categories(Transaction.EXPENSE),
                                           state="readonly", width=16)
        self.category_combo.grid(row=2, column=1, padx=6, pady=4)
        button_bar = ttk.Frame(form)
        button_bar.grid(row=2, column=2, columnspan=2, sticky=tk.E, padx=6, pady=4)
        ttk.Button(button_bar, text="Add", command=self._on_add_transaction).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_bar, text="Update Selected", command=self._on_update_transaction).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_bar, text="Delete Selected", command=self._on_delete_transaction).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_bar, text="Clear Form", command=self._clear_form).pack(side=tk.LEFT, padx=3)
        list_frame = ttk.LabelFrame(self.transactions_frame, text="All Transactions (newest first)")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        columns = ("date", "description", "category", "type", "amount")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("date", text="Date")
        self.tree.heading("description", text="Description")
        self.tree.heading("category", text="Category")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Amount")
        self.tree.column("date", width=100, anchor=tk.CENTER)
        self.tree.column("description", width=280, anchor=tk.W)
        self.tree.column("category", width=130, anchor=tk.W)
        self.tree.column("type", width=90, anchor=tk.CENTER)
        self.tree.column("amount", width=110, anchor=tk.E)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self._on_transaction_selected)
        self.summary_var = tk.StringVar(value="Income: 0.00 | Expenses: 0.00 | Savings: 0.00")
        ttk.Label(self.transactions_frame, textvariable=self.summary_var,
                  font=("TkDefault", 10, "bold")).pack(anchor=tk.W, padx=10, pady=4)
    def _on_type_changed(self, event=None):
        """Update the category list when the transaction type changes."""
        self.category_combo["values"] = Category.get_categories(self.type_var.get())
        if self.category_var.get() not in self.category_combo["values"]:
            self.category_var.set("")
    def _clear_form(self):
        """Reset the entry form to its default state."""
        self.selected_transaction_id = None
        self.date_var.set(date.today().strftime("%Y-%m-%d"))
        self.description_var.set("")
        self.amount_var.set("")
        self.type_var.set(Transaction.EXPENSE)
        self._on_type_changed()
        self.category_var.set("")
    def _on_add_transaction(self):
        """Handle the Add button: validate input and store a new transaction."""
        try:
            self.tracker.add_transaction(
                self.date_var.get(),
                self.description_var.get(),
                self.amount_var.get(),
                self.category_var.get(),
                self.type_var.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return
        self._clear_form()
        self.refresh_all()
    def _on_update_transaction(self):
        """Handle the Update button for the currently selected transaction."""
        if not self.selected_transaction_id:
            messagebox.showwarning("No Selection", "Please select a transaction to update.")
            return
        try:
            success = self.tracker.update_transaction(
                self.selected_transaction_id,
                self.date_var.get(),
                self.description_var.get(),
                self.amount_var.get(),
                self.category_var.get(),
                self.type_var.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return
        if success:
            self._clear_form()
            self.refresh_all()
        else:
            messagebox.showerror("Error", "Selected transaction no longer exists.")
    def _on_delete_transaction(self):
        """Handle the Delete button for the currently selected transaction."""
        if not self.selected_transaction_id:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete the selected transaction?"):
            return
        if self.tracker.delete_transaction(self.selected_transaction_id):
            self._clear_form()
            self.refresh_all()
    def _on_transaction_selected(self, event=None):
        """Load the selected transaction's values into the entry form."""
        selection = self.tree.selection()
        if not selection:
            return
        transaction_id = self.tree.item(selection[0], "tags")[0] if self.tree.item(selection[0], "tags") else None
        transaction = self.tracker.get_transaction(transaction_id)
        if transaction is None:
            return
        self.selected_transaction_id = transaction.id
        self.date_var.set(transaction.date)
        self.description_var.set(transaction.description)
        self.amount_var.set(str(transaction.amount))
        self.type_var.set(transaction.type)
        self._on_type_changed()
        self.category_var.set(transaction.category)
    # ------------------------------------------------------------------ #
    # Dashboard tab
    # ------------------------------------------------------------------ #
    def _build_dashboard_tab(self):
        """Build the dashboard with summary cards and charts."""
        cards = ttk.Frame(self.dashboard_frame)
        cards.pack(fill=tk.X, padx=8, pady=8)
        self.income_card_var = tk.StringVar(value="Total Income: 0.00")
        self.expense_card_var = tk.StringVar(value="Total Expenses: 0.00")
        self.savings_card_var = tk.StringVar(value="Total Savings: 0.00")
        for label, var in (("Income", self.income_card_var),
                           ("Expenses", self.expense_card_var),
                           ("Savings", self.savings_card_var)):
            card = ttk.LabelFrame(cards, text=label)
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
            ttk.Label(card, textvariable=var, font=("TkDefault", 12, "bold")).pack(padx=10, pady=8)
        self.chart_area = ttk.Frame(self.dashboard_frame)
        self.chart_area.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.pie_slot = ttk.Frame(self.chart_area)
        self.line_slot = ttk.Frame(self.chart_area)
        self.bar_slot = ttk.Frame(self.chart_area)
        self.pie_slot.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.line_slot.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.bar_slot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        if not MATPLOTLIB_AVAILABLE:
            ttk.Label(self.chart_area,
                      text="matplotlib is not installed - charts are disabled.\n"
                           "Install it with: pip install matplotlib",
                      foreground="red").pack(pady=20)
    def _render_dashboard_charts(self):
        """Rebuild all dashboard charts from current data."""
        for slot in (self.pie_slot, self.line_slot, self.bar_slot):
            for child in slot.winfo_children():
                child.destroy()
        if not MATPLOTLIB_AVAILABLE:
            return
        breakdown = self.tracker.get_category_breakdown()
        pie_fig = ChartGenerator.create_pie_chart(list(breakdown.keys()), list(breakdown.values()))
        FigureCanvasTkAgg(pie_fig, master=self.pie_slot).get_tk_widget().pack(fill=tk.BOTH, expand=True)
        labels, cumulative = self.tracker.get_savings_trend()
        line_fig = ChartGenerator.create_line_chart(labels, cumulative)
        FigureCanvasTkAgg(line_fig, master=self.line_slot).get_tk_widget().pack(fill=tk.BOTH, expand=True)
        monthly = self.tracker.get_monthly_summary()
        bar_fig = ChartGenerator.create_bar_chart(
            [entry["label"] for entry in monthly],
            [entry["income"] for entry in monthly],
            [entry["expenses"] for entry in monthly],
        )
        FigureCanvasTkAgg(bar_fig, master=self.bar_slot).get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # ------------------------------------------------------------------ #
    # Budgets tab
    # ------------------------------------------------------------------ #
    def _build_budget_tab(self):
        """Build the budget management controls and status table."""
        form = ttk.LabelFrame(self.budget_frame, text="Set Monthly Budget")
        form.pack(fill=tk.X, padx=8, pady=8)
        ttk.Label(form, text="Category:").grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)
        self.budget_category_var = tk.StringVar()
        self.budget_category_combo = ttk.Combobox(form, textvariable=self.budget_category_var,
                                                  values=Category.get_categories(Transaction.EXPENSE),
                                                  state="readonly", width=16)
        self.budget_category_combo.grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(form, text="Monthly Limit:").grid(row=0, column=2, sticky=tk.W, padx=6, pady=4)
        self.budget_amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.budget_amount_var, width=12).grid(row=0, column=3, padx=6, pady=4)
        ttk.Button(form, text="Save Budget", command=self._on_set_budget).grid(row=0, column=4, padx=6, pady=4)
        ttk.Button(form, text="Remove Budget", command=self._on_remove_budget).grid(row=0, column=5, padx=6, pady=4)
        status_frame = ttk.LabelFrame(self.budget_frame, text="Budget Status (current month)")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        columns = ("category", "budget", "spent", "remaining", "percent")
        self.budget_tree = ttk.Treeview(status_frame, columns=columns, show="headings")
        self.budget_tree.heading("category", text="Category")
        self.budget_tree.heading("budget", text="Budget")
        self.budget_tree.heading("spent", text="Spent")
        self.budget_tree.heading("remaining", text="Remaining")
        self.budget_tree.heading("percent", text="% Used")
        self.budget_tree.column("category", width=150, anchor=tk.W)
        self.budget_tree.column("budget", width=110, anchor=tk.E)
        self.budget_tree.column("spent", width=110, anchor=tk.E)
        self.budget_tree.column("remaining", width=110, anchor=tk.E)
        self.budget_tree.column("percent", width=90, anchor=tk.CENTER)
        self.budget_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        budget_scroll = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.budget_tree.yview)
        self.budget_tree.configure(yscrollcommand=budget_scroll.set)
        budget_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    def _on_set_budget(self):
        """Handle saving a category budget."""
        try:
            self.tracker.set_budget(self.budget_category_var.get(), self.budget_amount_var.get())
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return
        self.budget_amount_var.set("")
        self.refresh_all()
    def _on_remove_budget(self):
        """Handle removing a category budget."""
        if self.tracker.remove_budget(self.budget_category_var.get()):
            self.refresh_all()
        else:
            messagebox.showinfo("Not Found", "No budget exists for the selected category.")
    def _render_budget_status(self):
        """Refresh the budget status table for the current month."""
        self.budget_tree.delete(*self.budget_tree.get_children())
        today = date.today()
        for row in self.tracker.get_budget_status(today.year, today.month):
            self.budget_tree.insert("", tk.END, values=(
                row["category"],
                f"{row['budget']:.2f}",
                f"{row['spent']:.2f}",
                f"{row['remaining']:.2f}",
                f"{row['percent_used']:.1f}%",
            ))
    # ------------------------------------------------------------------ #
    # Reports tab
    # ------------------------------------------------------------------ #
    def _build_reports_tab(self):
        """Build the monthly report table."""
        frame = ttk.LabelFrame(self.reports_frame, text="Monthly Summary")
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        columns = ("month", "income", "expenses", "savings")
        self.report_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.report_tree.heading("month", text="Month")
        self.report_tree.heading("income", text="Income")
        self.report_tree.heading("expenses", text="Expenses")
        self.report_tree.heading("savings", text="Savings")
        self.report_tree.column("month", width=120, anchor=tk.CENTER)
        self.report_tree.column("income", width=140, anchor=tk.E)
        self.report_tree.column("expenses", width=140, anchor=tk.E)
        self.report_tree.column("savings", width=140, anchor=tk.E)
        self.report_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        report_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=report_scroll.set)
        report_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    def _render_reports(self):
        """Refresh the monthly summary table."""
        self.report_tree.delete(*self.report_tree.get_children())
        for entry in self.tracker.get_monthly_summary():
            self.report_tree.insert("", tk.END, values=(
                entry["label"],
                f"{entry['income']:.2f}",
                f"{entry['expenses']:.2f}",
                f"{entry['savings']:.2f}",
            ))
    # ------------------------------------------------------------------ #
    # Global refresh
    # ------------------------------------------------------------------ #
    def refresh_all(self):
        """Refresh every tab with the latest data."""
        self._render_transaction_list()
        self._render_summary_labels()
        self._render_dashboard_charts()
        self._render_budget_status()
        self._render_reports()
    def _render_transaction_list(self):
        """Refresh the transaction list view."""
        self.tree.delete(*self.tree.get_children())
        for transaction in self.tracker.get_all_transactions():
            self.tree.insert("", tk.END, values=(
                transaction.date,
                transaction.description,
                transaction.category,
                transaction.type.capitalize(),
                f"{transaction.amount:.2f}",
            ), tags=(transaction.id,))
    def _render_summary_labels(self):
        """Refresh the summary labels on the transactions tab and dashboard."""
        income = self.tracker.get_total_income()
        expenses = self.tracker.get_total_expenses()
        savings = self.tracker.get_savings()
        self.summary_var.set(f"Income: {income:.2f} | Expenses: {expenses:.2f} | Savings: {savings:.2f}")
        self.income_card_var.set(f"Total Income: {income:.2f}")
        self.expense_card_var.set(f"Total Expenses: {expenses:.2f}")
        self.savings_card_var.set(f"Total Savings: {savings:.2f}")