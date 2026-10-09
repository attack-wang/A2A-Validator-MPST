'''
dialogs.py
Modal dialog windows used to create and edit records.
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
EXPENSE_CATEGORIES = ["Food", "Rent", "Utilities", "Transport", "Entertainment",
                      "Health", "Shopping", "Education", "Travel", "Other"]
INCOME_CATEGORIES = ["Salary", "Bonus", "Freelance", "Investments", "Gifts", "Other"]
class _ModalDialog(tk.Toplevel):
    """Base class: builds a modal window with OK/Cancel buttons."""
    def __init__(self, master, title):
        super().__init__(master)
        self.result = None
        self.title(title)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.body = ttk.Frame(self, padding=10)
        self.body.pack(fill="both", expand=True)
        self._build_form()
        btns = ttk.Frame(self, padding=(10, 0, 10, 10))
        btns.pack(fill="x")
        ttk.Button(btns, text="OK", command=self._on_ok).pack(side="right", padx=4)
        ttk.Button(btns, text="Cancel", command=self._on_cancel).pack(side="right")
        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_cancel())
        self.wait_window(self)
    def _build_form(self):
        raise NotImplementedError
    def _collect(self):
        raise NotImplementedError
    def _on_ok(self):
        try:
            self.result = self._collect()
        except ValueError as exc:
            messagebox.showwarning("Invalid input", str(exc), parent=self)
            return
        self.destroy()
    def _on_cancel(self):
        self.result = None
        self.destroy()