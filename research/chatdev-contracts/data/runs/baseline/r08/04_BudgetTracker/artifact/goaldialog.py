class GoalDialog(_ModalDialog):
    def __init__(self, master, goal=None, title="Savings Goal"):
        self.goal = goal
        super().__init__(master, title)
    def _build_form(self):
        goal = self.goal
        self.name_var = tk.StringVar(value=goal.name if goal else "")
        self.target_var = tk.StringVar(value=f"{goal.target_amount:.2f}" if goal else "")
        self.current_var = tk.StringVar(value=f"{goal.current_amount:.2f}" if goal else "0.00")
        self.deadline_var = tk.StringVar(value=goal.deadline if goal and goal.deadline else "")
        form = self.body
        ttk.Label(form, text="Goal name").grid(row=0, column=0, sticky="e", pady=3, padx=(0, 8))
        ttk.Entry(form, textvariable=self.name_var, width=24).grid(row=0, column=1, pady=3)
        ttk.Label(form, text="Target amount").grid(row=1, column=0, sticky="e", pady=3, padx=(0, 8))
        ttk.Entry(form, textvariable=self.target_var, width=24).grid(row=1, column=1, pady=3)
        ttk.Label(form, text="Saved so far").grid(row=2, column=0, sticky="e", pady=3, padx=(0, 8))
        ttk.Entry(form, textvariable=self.current_var, width=24).grid(row=2, column=1, pady=3)
        ttk.Label(form, text="Deadline (optional)").grid(row=3, column=0, sticky="e", pady=3, padx=(0, 8))
        ttk.Entry(form, textvariable=self.deadline_var, width=24).grid(row=3, column=1, pady=3)
    def _collect(self):
        name = self.name_var.get().strip()
        if not name:
            raise ValueError("Please enter a goal name.")
        try:
            target = round(float(self.target_var.get()), 2)
        except ValueError:
            raise ValueError("Target amount must be a number, e.g. 1000.00")
        if target <= 0:
            raise ValueError("Target amount must be greater than zero.")
        try:
            current = round(float(self.current_var.get() or 0), 2)
        except ValueError:
            raise ValueError("Saved-so-far must be a number.")
        if current < 0:
            raise ValueError("Saved-so-far cannot be negative.")
        deadline = self.deadline_var.get().strip() or None
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Deadline must be in YYYY-MM-DD format.")
        return {"name": name, "target_amount": target,
                "current_amount": current, "deadline": deadline}