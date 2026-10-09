'''
gui.py
Tkinter GUI for the budget tracker.
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from visualizer import Visualizer, MATPLOTLIB_AVAILABLE
if MATPLOTLIB_AVAILABLE:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
CATEGORIES = ["Food", "Housing", "Transport", "Utilities", "Entertainment",
              "Health", "Shopping", "Education", "Other"]
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
    # ------------------------------------------------------------------
    # Expenses tab
    # ------------------------------------------------------------------
    def _build_expenses_tab(self):
        form = ttk.LabelFrame(self.expenses_frame, text="Add Expense")
        form.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(form, text="Amount:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.amount_var, width=12).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form, text="Category:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.category_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(form, textvariable=self.category_var, values=CATEGORIES,
                     state="readonly", width=15).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form, textvariable=self.date_var, width=12).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form, text="Description:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.description_var, width=25).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(form, text="Add Expense", command=self.add_expense).grid(
            row=2, column=0, columnspan=4, pady=8)
        list_frame = ttk.LabelFrame(self.expenses_frame, text="Recorded Expenses")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        columns = ("date", "category", "amount", "description")
        self.expense_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.expense_tree.heading("date", text="Date")
        self.expense_tree.heading("category", text="Category")
        self.expense_tree.heading("amount", text="Amount")
        self.expense_tree.heading("description", text="Description")
        self.expense_tree.column("date", width=110)
        self.expense_tree.column("category", width=120)
        self.expense_tree.column("amount", width=90, anchor=tk.E)
        self.expense_tree.column("description", width=300)
        self.expense_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)
        ttk.Button(self.expenses_frame, text="Delete Selected Expense",
                   command=self.delete_expense).pack(pady=(0, 10))
    def add_expense(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Invalid amount", "Please enter a valid number for the amount.")
            return
        date = self.date_var.get().strip() or None
        try:
            self.tracker.add_expense(
                amount=amount,
                category=self.category_var.get(),
                description=self.description_var.get().strip(),
                date=date,
            )
        except ValueError as exc:
            messagebox.showerror("Invalid expense", str(exc))
            return
        self.amount_var.set("")
        self.description_var.set("")
        self.refresh_all()
    def delete_expense(self):
        selected = self.expense_tree.selection()
        if not selected:
            messagebox.showinfo("No selection", "Select an expense to delete first.")
            return
        expense_id = selected[0]
        if self.tracker.remove_expense(expense_id):
            self.refresh_all()
    # ------------------------------------------------------------------
    # Savings tab
    # ------------------------------------------------------------------
    def _build_savings_tab(self):
        form = ttk.LabelFrame(self.savings_frame, text="Create Savings Goal")
        form.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(form, text="Goal name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.goal_name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.goal_name_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form, text="Target amount:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.goal_target_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.goal_target_var, width=12).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(form, text="Create Goal", command=self.add_goal).grid(
            row=1, column=0, columnspan=4, pady=8)
        list_frame = ttk.LabelFrame(self.savings_frame, text="Savings Goals")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        columns = ("name", "saved", "target", "progress")
        self.goal_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.goal_tree.heading("name", text="Goal")
        self.goal_tree.heading("saved", text="Saved")
        self.goal_tree.heading("target", text="Target")
        self.goal_tree.heading("progress", text="Progress")
        self.goal_tree.column("name", width=180)
        self.goal_tree.column("saved", width=110, anchor=tk.E)
        self.goal_tree.column("target", width=110, anchor=tk.E)
        self.goal_tree.column("progress", width=100, anchor=tk.E)
        self.goal_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.goal_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.goal_tree.configure(yscrollcommand=scrollbar.set)
        actions = ttk.Frame(self.savings_frame)
        actions.pack(pady=(0, 10))
        ttk.Label(actions, text="Amount:").pack(side=tk.LEFT, padx=5)
        self.transaction_var = tk.StringVar()
        ttk.Entry(actions, textvariable=self.transaction_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="Deposit", command=self.deposit).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="Withdraw", command=self.withdraw).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="Delete Selected Goal", command=self.delete_goal).pack(side=tk.LEFT, padx=15)
    def _selected_goal(self):
        selected = self.goal_tree.selection()
        if not selected:
            messagebox.showinfo("No selection", "Select a savings goal first.")
            return None
        return self.tracker.get_goal(selected[0])
    def add_goal(self):
        name = self.goal_name_var.get().strip()
        if not name:
            messagebox.showerror("Missing name", "Please enter a name for the goal.")
            return
        try:
            target = float(self.goal_target_var.get())
        except ValueError:
            messagebox.showerror("Invalid amount", "Please enter a valid number for the target.")
            return
        try:
            self.tracker.add_goal(name, target)
        except ValueError as exc:
            messagebox.showerror("Invalid goal", str(exc))
            return
        self.goal_name_var.set("")
        self.goal_target_var.set("")
        self.refresh_all()
    def _transaction(self, action):
        goal = self._selected_goal()
        if goal is None:
            return
        try:
            amount = float(self.transaction_var.get())
        except ValueError:
            messagebox.showerror("Invalid amount", "Please enter a valid number for the amount.")
            return
        try:
            if action == "deposit":
                self.tracker.deposit(goal.id, amount)
            else:
                self.tracker.withdraw(goal.id, amount)
        except ValueError as exc:
            messagebox.showerror("Transaction failed", str(exc))
            return
        self.transaction_var.set("")
        self.refresh_all()
    def deposit(self):
        self._transaction("deposit")
    def withdraw(self):
        self._transaction("withdraw")
    def delete_goal(self):
        goal = self._selected_goal()
        if goal is None:
            return
        if messagebox.askyesno("Delete goal", f"Delete goal '{goal.name}'?"):
            self.tracker.remove_goal(goal.id)
            self.refresh_all()
    # ------------------------------------------------------------------
    # Reports tab
    # ------------------------------------------------------------------
    def _build_reports_tab(self):
        if MATPLOTLIB_AVAILABLE:
            charts = ttk.Frame(self.reports_frame)
            charts.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.pie_canvas_holder = ttk.Frame(charts)
            self.pie_canvas_holder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.trend_canvas_holder = ttk.Frame(charts)
            self.trend_canvas_holder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.savings_canvas_holder = ttk.Frame(charts)
            self.savings_canvas_holder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            self.report_text = tk.Text(self.reports_frame, wrap=tk.WORD, font=("Consolas", 10))
            self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    def refresh_all(self):
        self.refresh_expenses()
        self.refresh_goals()
        self.refresh_reports()
    def refresh_expenses(self):
        self.expense_tree.delete(*self.expense_tree.get_children())
        for e in self.tracker.get_expenses_sorted():
            self.expense_tree.insert("", tk.END, iid=e.id,
                                     values=(e.date, e.category, f"{e.amount:.2f}", e.description))
    def refresh_goals(self):
        self.goal_tree.delete(*self.goal_tree.get_children())
        for g in self.tracker.savings_goals:
            status = "Complete!" if g.is_complete else f"{g.progress:.1f}%"
            self.goal_tree.insert("", tk.END, iid=g.id,
                                  values=(g.name, f"{g.saved_amount:.2f}",
                                          f"{g.target_amount:.2f}", status))
    def refresh_reports(self):
        if MATPLOTLIB_AVAILABLE:
            for holder, fig_method in (
                (self.pie_canvas_holder, "expense_pie_figure"),
                (self.trend_canvas_holder, "expense_trend_figure"),
                (self.savings_canvas_holder, "savings_progress_figure"),
            ):
                for child in holder.winfo_children():
                    child.destroy()
                fig = getattr(self.visualizer, fig_method)()
                canvas = FigureCanvasTkAgg(fig, master=holder)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            self.report_text.delete("1.0", tk.END)
            self.report_text.insert(tk.END, self.visualizer.text_summary())