class BudgetTrackerGUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self._chart_canvas = None
        self._chart_figure = None
        self._setup_window()
        self._build_notebook()
        self.refresh_all()
    def _setup_window(self):
        self.root.title("Budget Tracker – Expenses & Savings")
        self.root.geometry("900x640")
        self.root.minsize(820, 560)
        ...