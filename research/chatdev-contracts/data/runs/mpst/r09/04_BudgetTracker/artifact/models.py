def _selected_transaction(self):
    selection = self.transaction_tree.selection()
    if not selection:
        messagebox.showinfo("No selection", "Select a transaction first.")
        return None
    iid = selection[0]
    for t in self.transactions:
        if str(t.transaction_id) == iid:
            return t
    # Fallback: match by displayed values
    values = self.transaction_tree.item(iid, "values")
    date, ttype, category = values[0], values[1], values[2]
    for t in self.transactions:
        if (t.date == date and t.category == category
                and t.transaction_type == ttype.lower()):
            return t
    return None