def _run_persist(self, func, *args, **kwargs):
    """Run a manager operation, showing an error dialog if saving fails."""
    try:
        return func(*args, **kwargs)
    except IOError as exc:
        messagebox.showerror("Save error", str(exc))
        return None