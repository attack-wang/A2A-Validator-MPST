class BudgetTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Tracker — Expenses & Savings")
        self.geometry("1000x660")
        self.minsize(900, 600)
        self.data = DataManager()
        self._setup_style()
        self._build_ui()
        self.refresh_all()