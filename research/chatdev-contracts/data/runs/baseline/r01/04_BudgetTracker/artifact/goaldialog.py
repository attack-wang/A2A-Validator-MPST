class GoalDialog(tk.Toplevel):
    """Modal dialog for creating a new savings goal."""
    def __init__(self, master, on_saved=None):
        super().__init__(master)
        self.on_saved = on_saved
        self.result = None
        self.title("New Savings Goal")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.name_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.deadline_var = tk.StringVar()
        self._build_form()
        self.bind("<Return>", lambda event: self._save())
        self.bind("<Escape>", lambda event: self.destroy())
        self.name_entry.focus_set()
        self.wait_window()
    def _build_form(self):
        """Lay out the goal input fields and buttons."""
        frame = ttk.Frame(self, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")
        ttk.Label(frame, text="Goal name:").grid(row=0, column=0, sticky="w", pady=4)
        self.name_entry = ttk.Entry(frame, textvariable=self.name_var, width=26)
        self.name_entry.grid(row=0, column=1, sticky="we", pady=4)
        ttk.Label(frame, text="Target amount ($):").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.target_var, width=26).grid(row=1, column=1, sticky="we", pady=4)
        ttk.Label(frame, text="Deadline (YYYY-MM-DD, optional):").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.deadline_var, width=26).grid(row=2, column=1, sticky="we", pady=4)
        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(buttons, text="Save", command=self._save).pack(side="left", padx=4)
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="left", padx=4)
    def _save(self):
        """Validate input, build the SavingsGoal, notify the caller, close."""
        deadline = self.deadline_var.get().strip()
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Invalid input",
                    "Deadline must be empty or in YYYY-MM-DD format.",
                    parent=self)
                return
        try:
            goal = SavingsGoal(
                name=self.name_var.get(),
                target_amount=self.target_var.get(),
                deadline=deadline,
            )
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Invalid input", str(exc), parent=self)
            return
        self.result = goal
        if self.on_saved:
            self.on_saved(goal)
        self.destroy()