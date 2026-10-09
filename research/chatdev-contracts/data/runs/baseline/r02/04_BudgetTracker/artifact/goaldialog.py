class GoalDialog(tk.Toplevel):
    """Dialog to create a savings goal."""
    name entry, target entry; validate target > 0; result dict {"name":..., "target_amount":...}