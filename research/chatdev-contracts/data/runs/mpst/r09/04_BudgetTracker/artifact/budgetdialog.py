'''
budgetdialog.py
Budget dialog for the Budget Tracker application.
``BudgetDialog`` is a modal tkinter dialog used to create or edit a
monthly spending limit for one expense category. On successful
validation the new :class:`models.Budget` is exposed through the
``result`` attribute; ``result`` stays ``None`` when cancelled.
'''
import tkinter as tk
from tkinter import ttk, messagebox
from models import Budget
class BudgetDialog(tk.Toplevel):
    """Modal dialog to create or edit a monthly category budget."""
    def __init__(self, master, budget=None, existing_categories=(),
                 title="Add Budget"):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.result = None
        self.budget = budget
        self.category_var = tk.StringVar(
            value=budget.category if budget else "")
        self.limit_var = tk.StringVar(
            value="{:.2f}".format(budget.monthly_limit) if budget else "")
        self._build_form(existing_categories)
        self.bind("<Return>", lambda event: self._on_ok())
        self.bind("<Escape>", lambda event: self._on_cancel())
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        # Center the dialog over the parent window.
        self.update_idletasks()
        x = master.winfo_rootx() + max(0, (master.winfo_width()
                                           - self.winfo_width()) // 2)
        y = master.winfo_rooty() + max(0, (master.winfo_height()
                                           - self.winfo_height()) // 2)
        self.geometry("+{}+{}".format(x, y))
        self.wait_window()
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_form(self, existing_categories):
        """Create the category/limit fields and the OK/Cancel buttons."""
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Category:").grid(
            row=0, column=0, sticky="w", pady=3)
        category_box = ttk.Combobox(frame, textvariable=self.category_var,
                                    values=sorted(existing_categories),
                                    width=20)
        category_box.grid(row=0, column=1, sticky="we", pady=3)
        ttk.Label(frame, text="Monthly limit:").grid(
            row=1, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.limit_var, width=22).grid(
            row=1, column=1, sticky="we", pady=3)
        button_row = ttk.Frame(frame)
        button_row.grid(row=2, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(button_row, text="OK", command=self._on_ok).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="Cancel", command=self._on_cancel).pack(
            side=tk.LEFT, padx=5)
        frame.columnconfigure(1, weight=1)
    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_ok(self):
        """Validate the form and close, returning the Budget."""
        if not self.category_var.get().strip():
            messagebox.showerror("Invalid input",
                                 "Category cannot be empty.", parent=self)
            return
        try:
            budget = Budget(
                category=self.category_var.get(),
                monthly_limit=self.limit_var.get(),
                budget_id=(self.budget.budget_id if self.budget else None),
            )
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc), parent=self)
            return
        self.result = budget
        self.destroy()
    def _on_cancel(self):
        """Close the dialog without saving anything."""
        self.result = None
        self.destroy()