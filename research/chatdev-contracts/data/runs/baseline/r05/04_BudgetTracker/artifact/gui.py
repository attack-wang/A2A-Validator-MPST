'''
gui.py
Tkinter GUI for the Budget Tracker application.
Provides BudgetTrackerApp: a tabbed window (Transactions, Budgets,
Savings, Dashboard) that wires every user action to the BudgetTracker
core logic and renders charts via charts.ChartGenerator when matplotlib
is available (falling back to text summaries otherwise).
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tracker import BudgetTracker
from charts import ChartGenerator, MATPLOTLIB_AVAILABLE
DATE_FORMAT = "%Y-%m-%d"
class BudgetTrackerApp:
    """Main application window with tabbed interface."""
    def __init__(self, root):
        self.root = root
        self.tracker = BudgetTracker()
        self.setup_window()
        self.create_widgets()
        self.refresh_all()
    def setup_window(self):
        """Configure the root window's title and default size."""
        self.root.title("Budget Tracker")
        self.root.geometry("900x650")
        self.root.minsize(820, 600)
    def create_widgets(self):
        """Create the tabbed notebook and all four feature tabs."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.build_transactions_tab()
        self.build_budgets_tab()
        self.build_savings_tab()
        self.build_dashboard_tab()
    # ------------------------------------------------------------------
    # Transactions tab
    # ------------------------------------------------------------------
    def build_transactions_tab(self):
        # ... same as provided ...
        # populate category combo
        self.category_combo["values"] = self.tracker.get_categories()
        if self.tracker.get_categories():
            self.category_combo.current(0)
    def on_add_transaction(self):
        # ... same as provided ...
    def on_delete_transaction(self):
        # ... same as provided ...
    # ------------------------------------------------------------------
    # Budgets tab
    # ------------------------------------------------------------------
    def build_budgets_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Budgets")
        form = ttk.LabelFrame(frame, text="Set Monthly Budget", padding=8)
        form.pack(fill=tk.X)
        ttk.Label(form, text="Category:").grid(row=0, column=0, sticky=tk.W)
        self.budget_category_combo = ttk.Combobox(form, width=16, state="readonly")
        self.budget_category_combo.grid(row=0, column=1, padx=5, pady=3)
        ttk.Label(form, text="Monthly Limit:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.budget_limit_entry = ttk.Entry(form, width=12)
        self.budget_limit_entry.grid(row=0, column=3, padx=5, pady=3)
        ttk.Button(form, text="Save Budget", command=self.on_set_budget).grid(row=0, column=4, padx=5, pady=3)
        list_frame = ttk.LabelFrame(frame, text="Budget Status (Current Month)", padding=8)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        columns = ("category", "limit", "spent", "remaining", "status")
        self.budget_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col, width in (("category", 140), ("limit", 110), ("spent", 110),
                           ("remaining", 110), ("status", 100)):
            self.budget_tree.heading(col, text=col.capitalize())
            self.budget_tree.column(col, width=width, anchor=tk.W)
        self.budget_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.budget_tree.yview)
        self.budget_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Button(frame, text="Delete Selected Budget",
                   command=self.on_delete_budget).pack(pady=6)
    def on_set_budget(self):
        category = self.budget_category_combo.get()
        ok, message = self.tracker.set_budget(category, self.budget_limit_entry.get().strip())
        if ok:
            self.budget_limit_entry.delete(0, tk.END)
            self.refresh_all()
        else:
            messagebox.showwarning("Invalid input", message)
    def on_delete_budget(self):
        selection = self.budget_tree.selection()
        if not selection:
            messagebox.showinfo("Delete", "Select a budget first.")
            return
        # iid stores the category name
        if self.tracker.remove_budget(selection[0]):
            self.refresh_all()
    # ------------------------------------------------------------------
    # Savings tab
    # ------------------------------------------------------------------
    def build_savings_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Savings")
        form = ttk.LabelFrame(frame, text="Create Savings Goal", padding=8)
        form.pack(fill=tk.X)
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.goal_name_entry = ttk.Entry(form, width=20)
        self.goal_name_entry.grid(row=0, column=1, padx=5, pady=3)
        ttk.Label(form, text="Target Amount:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.goal_target_entry = ttk.Entry(form, width=12)
        self.goal_target_entry.grid(row=0, column=3, padx=5, pady=3)
        ttk.Label(form, text="Deadline (optional):").grid(row=1, column=0, sticky=tk.W)
        self.goal_deadline_entry = ttk.Entry(form, width=12)
        self.goal_deadline_entry.grid(row=1, column=1, padx=5, pady=3)
        ttk.Button(form, text="Create Goal", command=self.on_add_goal).grid(row=1, column=2, columnspan=2, padx=5, pady=3, sticky=tk.E)
        contribute_form = ttk.LabelFrame(frame, text="Contribute to Goal", padding=8)
        contribute_form.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(contribute_form, text="Goal:").grid(row=0, column=0, sticky=tk.W)
        self.goal_combo = ttk.Combobox(contribute_form, width=24, state="readonly")
        self.goal_combo.grid(row=0, column=1, padx=5, pady=3)
        ttk.Label(contribute_form, text="Amount:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.contribution_entry = ttk.Entry(contribute_form, width=12)
        self.contribution_entry.grid(row=0, column=3, padx=5, pady=3)
        ttk.Button(contribute_form, text="Contribute", command=self.on_contribute).grid(row=0, column=4, padx=5, pady=3)
        list_frame = ttk.LabelFrame(frame, text="Savings Goals", padding=8)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        columns = ("name", "saved", "target", "remaining", "progress")
        self.goal_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col, width in (("name", 200), ("saved", 110), ("target", 110),
                           ("remaining", 110), ("progress", 90)):
            self.goal_tree.heading(col, text=col.capitalize())
            self.goal_tree.column(col, width=width, anchor=tk.W)
        self.goal_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.goal_tree.yview)
        self.goal_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Button(frame, text="Delete Selected Goal",
                   command=self.on_delete_goal).pack(pady=6)
    def on_add_goal(self):
        ok, message = self.tracker.add_goal(
            name=self.goal_name_entry.get(),
            target_amount=self.goal_target_entry.get().strip(),
            deadline=self.goal_deadline_entry.get().strip() or None,
        )
        if ok:
            self.goal_name_entry.delete(0, tk.END)
            self.goal_target_entry.delete(0, tk.END)
            self.goal_deadline_entry.delete(0, tk.END)
            self.refresh_all()
        else:
            messagebox.showwarning("Invalid input", message)
    def on_contribute(self):
        goal_id = self._selected_goal_id()
        if not goal_id:
            messagebox.showinfo("Contribute", "Select a goal first.")
            return
        ok, message = self.tracker.contribute_to_goal(goal_id, self.contribution_entry.get().strip())
        if ok:
            self.contribution_entry.delete(0, tk.END)
            self.refresh_all()
            messagebox.showinfo("Contribution", message)  # maybe
        else:
            messagebox.showwarning("Invalid input", message)
    def _selected_goal_id(self):
        """Map the selected goal row back to its id via the iid."""
        selection = self.goal_tree.selection()
        return selection[0] if selection else None
    def on_delete_goal(self):
        selection = self.goal_tree.selection()
        if not selection:
            messagebox.showinfo("Delete", "Select a goal first.")
            return
        if self.tracker.remove_goal(selection[0]):
            self.refresh_all()
    # ------------------------------------------------------------------
    # Dashboard tab
    # ------------------------------------------------------------------
    def build_dashboard_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Dashboard")
        summary_frame = ttk.LabelFrame(frame, text="This Month Summary", padding=8)
        summary_frame.pack(fill=tk.X)
        self.summary_label = ttk.Label(summary_frame, text="", font=("", 11))
        self.summary_label.pack(anchor=tk.W)
        self.charts_frame = ttk.LabelFrame(frame, text="Charts", padding=8)
        self.charts_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.fallback_text = tk.Text(self.charts_frame, height=10, wrap=tk.WORD,
                                     state=tk.DISABLED)
    def refresh_dashboard(self):
        """Rebuild the dashboard summary and charts."""
        month = datetime.now().strftime("%Y-%m")
        income, expenses, net = self.tracker.monthly_summary(month)
        self.summary_label.config(
            text=f"Income: {income:.2f}   Expenses: {expenses:.2f}   "
                 f"Net Savings: {net:.2f}")
        # Clear previous charts/widgets before redrawing.
        for child in self.charts_frame.winfo_children():
            child.destroy()
        if MATPLOTLIB_AVAILABLE:
            self._render_charts()
        else:
            self._render_text_summary()
    def _render_charts(self):
        """Draw all dashboard charts with matplotlib."""
        months = self.tracker.recent_months(6)
        income_values, expense_values = [], []
        for month in months:
            income, expenses, _ = self.tracker.monthly_summary(month)
            income_values.append(income)
            expense_values.append(expenses)
        pie = ChartGenerator.expense_pie_chart(self.tracker.category_totals())
        bar = ChartGenerator.monthly_bar_chart(months, income_values, expense_values)
        ChartGenerator.embed_chart(pie, self.charts_frame)
        ChartGenerator.embed_chart(bar, self.charts_frame)
        _, savings_values = self.tracker.savings_by_month(6)
        line = ChartGenerator.savings_line_chart(months, savings_values)
        ChartGenerator.embed_chart(line, self.charts_frame)
        progress = ChartGenerator.goal_progress_chart(self.tracker.goal_progress())
        ChartGenerator.embed_chart(progress, self.charts_frame)
    def _render_text_summary(self):
        """Fallback dashboard when matplotlib is unavailable."""
        self.fallback_text = tk.Text(self.charts_frame, wrap=tk.WORD)
        lines = ["(matplotlib not installed - text summary shown)", ""]
        months = self.tracker.recent_months(6)
        for month in months:
            income, expenses, net = self.tracker.monthly_summary(month)
            lines.append(f"{month}:  income {income:.2f} | expenses {expenses:.2f} | net {net:.2f}")
        lines.append("")
        for name, saved, target, percent in self.tracker.goal_progress():
            lines.append(f"Goal '{name}': {saved:.2f} / {target:.2f} ({percent:.0f}%)")
        self.fallback_text.insert("1.0", "\n".join(lines))
        self.fallback_text.config(state=tk.DISABLED)
        self.fallback_text.pack(fill=tk.BOTH, expand=True)
    # ------------------------------------------------------------------
    # Refresh helpers
    # ------------------------------------------------------------------
    def refresh_transactions(self):
        """Reload the transaction table from the tracker."""
        self.tx_tree.delete(*self.tx_tree.get_children())
        for t in self.tracker.transactions:
            sign = "" if t.type == "expense" else "+"
            self.tx_tree.insert("", tk.END, iid=t.id,
                                values=(t.date, t.description, t.category,
                                        t.type, f"{sign}{t.amount:.2f}"))
    def refresh_budgets(self):
        """Reload the budget status table and category combos."""
        self.budget_tree.delete(*self.budget_tree.get_children())
        for row in self.tracker.budget_status():
            status = "Over!" if row["over"] else "OK"
            self.budget_tree.insert("", tk.END, iid=row["category"],
                                    values=(row["category"], f"{row['limit']:.2f}",
                                            f"{row['spent']:.2f}",
                                            f"{row['remaining']:.2f}", status))
    def refresh_goals(self):
        """Reload the savings goal table and goal combo."""
        self.goal_tree.delete(*self.goal_tree.get_children())
        self.goal_combo.set("")
        self.goal_combo["values"] = [g.name for g in self.tracker.goals]
        for g in self.tracker.goals:
            self.goal_tree.insert("", tk.END, iid=g.id,
                                  values=(g.name, f"{g.saved_amount:.2f}",
                                          f"{g.target_amount:.2f}",
                                          f"{g.remaining_amount():.2f}",
                                          f"{g.progress_percent():.0f}%"))
    def refresh_all(self):
        """Refresh every tab after any data change."""
        self.refresh_transactions()
        self.refresh_budgets()
        self.refresh_goals()
        self.refresh_dashboard()