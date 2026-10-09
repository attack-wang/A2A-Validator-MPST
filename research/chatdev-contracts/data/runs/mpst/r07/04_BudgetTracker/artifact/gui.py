"""
gui.py
Tkinter GUI for the Budget Tracker application.
Builds a tabbed interface (Dashboard / Expenses / Savings / Settings)
and wires all user actions to the BudgetTracker business logic.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
class BudgetTrackerGUI:
    """Main application window with four tabs wired to BudgetTracker."""
    def __init__(self, root, tracker, chart_gen):
        self.root = root
        self.tracker = tracker
        self.charts = chart_gen
        self._build_notebook()
        self.refresh_all()
    # -- layout ---------------------------------------------------------
    def _build_notebook(self):
        """Create the tab container and add all four tabs."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self._build_dashboard_tab()
        self._build_expenses_tab()
        self._build_savings_tab()
        self._build_settings_tab()
    def _build_dashboard_tab(self):
        """Summary text plus buttons that open the four chart windows."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")
        self.summary_var = tk.StringVar(value="")
        ttk.Label(frame, textvariable=self.summary_var, font=("Helvetica", 12),
                  justify="left").pack(pady=15, padx=15, anchor="w")
        buttons = ttk.Frame(frame)
        buttons.pack(pady=10)
        for text, cmd in (("Spending by Category", self._show_pie_chart),
                          ("Monthly Trend", self._show_trend_chart),
                          ("Budget Comparison", self._show_comparison_chart),
                          ("Savings Goals", self._show_goals_chart)):
            ttk.Button(buttons, text=text, command=cmd).pack(side=tk.LEFT, padx=6)
    def _build_expenses_tab(self):
        """Expense entry form and the expense table."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Expenses")
        form = ttk.LabelFrame(frame, text="Expense details")
        form.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(form, text="Amount:").grid(row=0, column=0, sticky="e", padx=4, pady=3)
        self.amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.amount_var, width=12).grid(row=0, column=1, padx=4)
        ttk.Label(form, text="Category:").grid(row=0, column=2, sticky="e", padx=4)
        self.category_var = tk.StringVar(value=self.tracker.DEFAULT_CATEGORIES[0])
        ttk.Combobox(form, textvariable=self.category_var, width=15,
                     values=self.tracker.DEFAULT_CATEGORIES,
                     state="readonly").grid(row=0, column=3, padx=4)
        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=4, sticky="e", padx=4)
        self.date_var = tk.StringVar(value=date.today().isoformat())
        ttk.Entry(form, textvariable=self.date_var, width=12).grid(row=0, column=5, padx=4)
        ttk.Label(form, text="Description:").grid(row=1, column=0, sticky="e", padx=4)
        self.desc_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.desc_var, width=40).grid(
            row=1, column=1, columnspan=5, sticky="we", padx=4)
        actions = ttk.Frame(form)
        actions.grid(row=2, column=0, columnspan=6, pady=6)
        ttk.Button(actions, text="Add", command=self._on_add_expense).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text="Update selected", command=self._on_update_expense).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text="Delete selected", command=self._on_delete_expense).pack(side=tk.LEFT, padx=4)
        columns = ("date", "category", "amount", "description", "id")
        self.expense_tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, text, width, anchor in (("date", "Date", 100, "w"),
                                         ("category", "Category", 120, "w"),
                                         ("amount", "Amount", 100, "e"),
                                         ("description", "Description", 280, "w"),
                                         ("id", "ID", 90, "w")):
            self.expense_tree.heading(col, text=text)
            self.expense_tree.column(col, width=width, anchor=anchor)
        self.expense_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.expense_tree.bind("<<TreeviewSelect>>", self._on_expense_select)
    def _build_savings_tab(self):
        """Savings-goal form, contribution controls, and the goals table."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Savings")
        form = ttk.LabelFrame(frame, text="Goal details")
        form.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="e", padx=4, pady=3)
        self.goal_name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.goal_name_var, width=20).grid(row=0, column=1, padx=4)
        ttk.Label(form, text="Target ($):").grid(row=0, column=2, sticky="e", padx=4)
        self.goal_target_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.goal_target_var, width=12).grid(row=0, column=3, padx=4)
        ttk.Label(form, text="Deadline (YYYY-MM-DD, optional):").grid(row=0, column=4, sticky="e", padx=4)
        self.goal_deadline_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.goal_deadline_var, width=12).grid(row=0, column=5, padx=4)
        ttk.Label(form, text="Contribute / withdraw ($):").grid(row=1, column=0, sticky="e", padx=4)
        self.goal_amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.goal_amount_var, width=12).grid(row=1, column=1, padx=4)
        actions = ttk.Frame(form)
        actions.grid(row=2, column=0, columnspan=6, pady=6)
        ttk.Button(actions, text="Add goal", command=self._on_add_goal).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text="Contribute", command=self._on_contribute).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text="Withdraw", command=self._on_withdraw).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text="Delete goal", command=self._on_delete_goal).pack(side=tk.LEFT, padx=4)
        columns = ("name", "target", "saved", "progress", "deadline", "id")
        self.goal_tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, text, width, anchor in (("name", "Goal", 160, "w"),
                                         ("target", "Target", 100, "e"),
                                         ("saved", "Saved", 100, "e"),
                                         ("progress", "Progress", 120, "w"),
                                         ("deadline", "Deadline", 100, "w"),
                                         ("id", "ID", 90, "w")):
            self.goal_tree.heading(col, text=text)
            self.goal_tree.column(col, width=width, anchor=anchor)
        self.goal_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.goal_tree.bind("<<TreeviewSelect>>", self._on_goal_select)
    def _build_settings_tab(self):
        """Monthly budget input and save button."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Settings")
        box = ttk.LabelFrame(frame, text="Monthly budget")
        box.pack(padx=10, pady=10, anchor="w")
        ttk.Label(box, text="Monthly budget ($):").grid(row=0, column=0, padx=6, pady=6)
        self.budget_var = tk.StringVar(value=f"{self.tracker.monthly_budget:.2f}")
        ttk.Entry(box, textvariable=self.budget_var, width=12).grid(row=0, column=1, padx=6)
        ttk.Button(box, text="Save", command=self._on_save_budget).grid(row=0, column=2, padx=6)
    # -- refresh ---------------------------------------------------------
    def refresh_all(self):
        """Reload every tab from the tracker's current state."""
        self._refresh_dashboard()
        self._refresh_expense_table()
        self._refresh_goal_table()
        self.budget_var.set(f"{self.tracker.monthly_budget:.2f}")
    def _refresh_dashboard(self):
        """Update the dashboard summary text."""
        spent = self.tracker.get_month_spent()
        budget = self.tracker.monthly_budget
        saved = sum(g.saved_amount for g in self.tracker.savings_goals)
        lines = [f"Spent this month: ${spent:,.2f}"]
        if budget > 0:
            remaining = budget - spent
            status = f"Remaining budget: ${remaining:,.2f}" if remaining >= 0 else \
                     f"Over budget by: ${-remaining:,.2f}"
            lines.append(status)
        else:
            lines.append("Monthly budget not set (set it in Settings).")
        lines.append(f"Total saved toward goals: ${saved:,.2f}")
        done = sum(1 for g in self.tracker.savings_goals if g.is_complete)
        lines.append(f"Goals completed: {done}/{len(self.tracker.savings_goals)}")
        self.summary_var.set("\n".join(lines))
    def _refresh_expense_table(self):
        """Rebuild the expense table rows."""
        self.expense_tree.delete(*self.expense_tree.get_children())
        for e in sorted(self.tracker.expenses, key=lambda x: (x.date_str, x.expense_id), reverse=True):
            self.expense_tree.insert("", tk.END, iid=e.expense_id, values=(
                e.date_str, e.category, f"${e.amount:,.2f}", e.description, e.expense_id))
    def _refresh_goal_table(self):
        """Rebuild the savings-goal table rows."""
        self.goal_tree.delete(*self.goal_tree.get_children())
        for g in self.tracker.savings_goals:
            self.goal_tree.insert("", tk.END, iid=g.goal_id, values=(
                g.name, f"${g.target_amount:,.2f}", f"${g.saved_amount:,.2f}",
                f"{g.progress * 100:.0f}%", g.deadline_str or "—", g.goal_id))