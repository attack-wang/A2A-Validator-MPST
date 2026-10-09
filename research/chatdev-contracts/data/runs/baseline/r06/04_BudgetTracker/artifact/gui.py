'''
gui.py
Tkinter graphical interface for the budget tracker.
Tabs: Transactions, Budget, Savings Goals and Charts.
All changes are persisted automatically via StorageManager.
'''
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from models import Transaction, SavingsGoal, Budget
from storage import StorageManager
import analytics
from charts import draw_pie_chart, draw_bar_chart
CATEGORIES = ["Food", "Transport", "Housing", "Utilities", "Entertainment",
              "Health", "Shopping", "Education", "Other"]
class BudgetTrackerGUI:
    """Main application window for the budget tracker."""
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("900x640")
        self.root.minsize(820, 560)
        self.storage = StorageManager()
        self.transactions, self.goals, self.budget = self.storage.load()
        self.editing_tx_id = None
        self._build_menu()
        self._build_header()
        self._build_tabs()
        self._build_status_bar()
        self.refresh_all()
    # ------------------------------------------------------------------ menu
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Backup data now", command=self.backup_data)
        file_menu.add_command(label="Clear all data...", command=self.clear_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)
    # ---------------------------------------------------------------- header
    def _build_header(self):
        header = ttk.Frame(self.root, padding=(10, 8))
        header.pack(fill="x")
        self.month_var = tk.StringVar(value=analytics.current_month())
        ttk.Label(header, text="Month:").pack(side="left")
        self.month_combo = ttk.Combobox(header, textvariable=self.month_var,
                                        state="readonly", width=10)
        self.month_combo.pack(side="left", padx=(4, 12))
        self.month_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_all())
        self.summary_var = tk.StringVar(value="No transactions yet.")
        ttk.Label(header, textvariable=self.summary_var,
                  font=("Helvetica", 10, "bold")).pack(side="left")
    # ------------------------------------------------------------------ tabs
    def _build_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        self.transactions_frame = ttk.Frame(notebook, padding=8)
        self.budget_frame = ttk.Frame(notebook, padding=8)
        self.goals_frame = ttk.Frame(notebook, padding=8)
        self.charts_frame = ttk.Frame(notebook, padding=8)
        notebook.add(self.transactions_frame, text="Transactions")
        notebook.add(self.budget_frame, text="Budget")
        notebook.add(self.goals_frame, text="Savings Goals")
        notebook.add(self.charts_frame, text="Charts")
        self._build_transactions_tab()
        self._build_budget_tab()
        self._build_goals_tab()
        self._build_charts_tab()
    # ------------------------------------------------------- transactions tab
    def _build_transactions_tab(self):
        form = ttk.LabelFrame(self.transactions_frame, text="Add transaction", padding=8)
        form.pack(fill="x")
        self.tx_kind_var = tk.StringVar(value="expense")
        self.tx_amount_var = tk.StringVar()
        self.tx_category_var = tk.StringVar(value=CATEGORIES[0])
        self.tx_description_var = tk.StringVar()
        self.tx_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Label(form, text="Type").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        ttk.Combobox(form, textvariable=self.tx_kind_var,
                     values=["expense", "income"], state="readonly", width=10).grid(row=0, column=1, sticky="w", padx=4, pady=2)
        ttk.Label(form, text="Amount").grid(row=0, column=2, sticky="e", padx=4, pady=2)
        ttk.Entry(form, textvariable=self.tx_amount_var, width=12).grid(row=0, column=3, sticky="w", padx=4, pady=2)
        ttk.Label(form, text="Category").grid(row=0, column=4, sticky="e", padx=4, pady=2)
        self.tx_category_combo = ttk.Combobox(form, textvariable=self.tx_category_var,
                                              values=CATEGORIES, state="readonly", width=14)
        self.tx_category_combo.grid(row=0, column=5, sticky="w", padx=4, pady=2)
        ttk.Label(form, text="Description").grid(row=1, column=0, sticky="w", padx=4, pady=2)
        ttk.Entry(form, textvariable=self.tx_description_var, width=32).grid(row=1, column=1, columnspan=3, sticky="we", padx=4, pady=2)
        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=1, column=4, sticky="e", padx=4, pady=2)
        ttk.Entry(form, textvariable=self.tx_date_var, width=12).grid(row=1, column=5, sticky="w", padx=4, pady=2)
        self.add_tx_button = ttk.Button(form, text="Add", command=self.add_transaction)
        self.add_tx_button.grid(row=0, column=6, rowspan=2, padx=8, sticky="ns")
        list_frame = ttk.Frame(self.transactions_frame)
        list_frame.pack(fill="both", expand=True, pady=(8, 0))
        columns = ("date", "kind", "category", "description", "amount")
        self.tx_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col, text, width in (("date", "Date", 90), ("kind", "Type", 70),
                                 ("category", "Category", 110),
                                 ("description", "Description", 280),
                                 ("amount", "Amount", 90)):
            self.tx_tree.heading(col, text=text)
            self.tx_tree.column(col, width=width, anchor="w")
        self.tx_tree.tag_configure("income", foreground="#1B7A43")
        self.tx_tree.tag_configure("expense", foreground="#B02418")
        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.tx_tree.yview)
        self.tx_tree.configure(yscrollcommand=scroll.set)
        self.tx_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        buttons = ttk.Frame(self.transactions_frame)
        buttons.pack(fill="x", pady=(6, 0))
        ttk.Button(buttons, text="Edit selected", command=self.edit_selected_transaction).pack(side="left")
        ttk.Button(buttons, text="Delete selected", command=self.delete_selected_transaction).pack(side="left", padx=6)
    def add_transaction(self):
        try:
            tx = Transaction(
                kind=self.tx_kind_var.get(),
                amount=self.tx_amount_var.get(),
                category=self.tx_category_var.get(),
                description=self.tx_description_var.get(),
                date_value=self.tx_date_var.get(),
                transaction_id=self.editing_tx_id,
            )
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return
        if self.editing_tx_id:
            self.transactions = [tx if t.id == self.editing_tx_id else t for t in self.transactions]
            self.status_var.set("Transaction updated.")
        else:
            self.transactions.append(tx)
            self.status_var.set("Transaction added.")
        self._reset_tx_form()
        self._persist()
        self.refresh_all()
    def edit_selected_transaction(self):
        selection = self.tx_tree.selection()
        if not selection:
            messagebox.showinfo("Edit transaction", "Select a transaction first.")
            return
        tx_id = selection[0]
        tx = next((t for t in self.transactions if t.id == tx_id), None)
        if tx is None:
            return
        self.editing_tx_id = tx_id
        self.tx_kind_var.set(tx.kind)
        self.tx_amount_var.set(f"{tx.amount:.2f}")
        self.tx_category_var.set(tx.category if tx.category in CATEGORIES else "Other")
        self.tx_description_var.set(tx.description)
        self.tx_date_var.set(tx.date)
        self.add_tx_button.config(text="Save changes")
        self.status_var.set(f"Editing transaction {tx_id}; press 'Save changes' when done.")
    def delete_selected_transaction(self):
        selection = self.tx_tree.selection()
        if not selection:
            messagebox.showinfo("Delete transaction", "Select a transaction first.")
            return
        tx_id = selection[0]
        self.transactions = [t for t in self.transactions if t.id != tx_id]
        if self.editing_tx_id == tx_id:
            self._reset_tx_form()
        self._persist()
        self.refresh_all()
        self.status_var.set("Transaction deleted.")
    def _reset_tx_form(self):
        self.editing_tx_id = None
        self.add_tx_button.config(text="Add")
        self.tx_amount_var.set("")
        self.tx_description_var.set("")
        self.tx_date_var.set(datetime.now().strftime("%Y-%m-%d"))