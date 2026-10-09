class TransactionDialog(tk.Toplevel):
    """Modal dialog to add or edit a transaction."""
    def __init__(self, parent, title="Add transaction", transaction=None, categories_expense=..., categories_income=...):
        ...
        result: self.result = dict or None