'''
gui.py
Transaction dialog for the Budget Tracker application.
``TransactionDialog`` is a modal tkinter dialog used to create or edit
a single income/expense record. On successful validation the new
:class:`models.Transaction` is exposed through the ``result``
attribute; ``result`` stays ``None`` when the dialog is cancelled.
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import (Transaction, DEFAULT_CATEGORIES, TRANSACTION_TYPES,
                    DATE_FORMAT)
class TransactionDialog(tk.Toplevel):
    """Modal dialog to create or edit a transaction."""
    def __init__(self, master, transaction=None, title="Add Transaction"):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.result = None
        self.transaction = transaction
        # Pre-fill the form when editing an existing record.
        self.type_var = tk.StringVar(
            value=transaction.transaction_type if transaction else "expense")
        self.date_var = tk.StringVar(
            value=transaction.date if transaction
            else datetime.now().strftime(DATE_FORMAT))
        self.category_var = tk.StringVar(
            value=transaction.category if transaction else "")
        self.amount_var = tk.StringVar(
            value="{:.2f}".format(transaction.amount) if transaction else "")
        self.description_var = tk.StringVar(
            value=transaction.description if transaction else "")
        self._build_form()
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
    def _build_form(self):
        """Create the labelled input fields and the OK/Cancel buttons."""
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Type:").grid(row=0, column=0, sticky="w", pady=3)
        type_box = ttk.Combobox(frame, textvariable=self.type_var,
                                values=list(TRANSACTION_TYPES),
                                state="readonly", width=20)
        type_box.grid(row=0, column=1, sticky="we", pady=3)
        type_box.bind("<<ComboboxSelected>>",
                      lambda event: self._on_type_change())
        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(
            row=1, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.date_var, width=22).grid(
            row=1, column=1, sticky="we", pady=3)
        ttk.Label(frame, text="Category:").grid(
            row=2, column=0, sticky="w", pady=3)
        self.category_box = ttk.Combobox(frame, textvariable=self.category_var,
                                         width=20)
        self.category_box.grid(row=2, column=1, sticky="we", pady=3)
        ttk.Label(frame, text="Amount:").grid(
            row=3, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.amount_var, width=22).grid(
            row=3, column=1, sticky="we", pady=3)
        ttk.Label(frame, text="Description:").grid(
            row=4, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.description_var, width=22).grid(
            row=4, column=1, sticky="we", pady=3)
        button_row = ttk.Frame(frame)
        button_row.grid(row=5, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(button_row, text="OK", command=self._on_ok).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="Cancel", command=self._on_cancel).pack(
            side=tk.LEFT, padx=5)
        frame.columnconfigure(1, weight=1)
        # Populate the category list for the initially selected type.
        self._on_type_change()
    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_type_change(self):
        """Refresh the category suggestions to match the selected type."""
        categories = DEFAULT_CATEGORIES.get(self.type_var.get(), [])
        self.category_box["values"] = categories
        current = self.category_var.get()
        if current not in categories:
            # When editing, keep a custom category; otherwise preselect.
            if self.transaction is None and categories:
                self.category_var.set(categories[0])
    def _on_ok(self):
        """Validate the form and close, returning the Transaction."""
        try:
            transaction = Transaction(
                date=self.date_var.get(),
                category=self.category_var.get(),
                amount=self.amount_var.get(),
                description=self.description_var.get(),
                transaction_type=self.type_var.get(),
                transaction_id=(self.transaction.transaction_id
                                if self.transaction else None),
            )
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc), parent=self)
            return
        self.result = transaction
        self.destroy()
    def _on_cancel(self):
        """Close the dialog without saving anything."""
        self.result = None
        self.destroy()