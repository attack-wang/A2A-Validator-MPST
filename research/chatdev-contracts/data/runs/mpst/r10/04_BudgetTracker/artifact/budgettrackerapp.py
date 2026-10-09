    def _build_dashboard_tab(self):
        self.dashboard_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        # --- Summary cards ---
        summary = ttk.Frame(self.dashboard_tab)
        summary.pack(fill="x", pady=(0, 10))
        self.total_savings_var = tk.StringVar(value="$0.00")
        self.total_expenses_var = tk.StringVar(value="$0.00")
        self.net_balance_var = tk.StringVar(value="$0.00")
        cards = [
            ("Total Savings", self.total_savings_var, "#2ecc71"),
            ("Total Expenses", self.total_expenses_var, "#e74c3c"),
            ("Net Balance", self.net_balance_var, "#3498db"),
        ]
        for i, (title, var, color) in enumerate(cards):
            card = ttk.LabelFrame(summary, text=title, padding=10)
            card.grid(row=0, column=i, sticky="nsew", padx=6)
            ttk.Label(card, textvariable=var, foreground=color,
                      style="SummaryValue.TLabel").pack()
            summary.columnconfigure(i, weight=1)
        # --- Savings goal ---
        goal_frame = ttk.LabelFrame(self.dashboard_tab, text="Savings Goal", padding=10)
        goal_frame.pack(fill="x", pady=(0, 10))
        self.goal_var = tk.StringVar(value="No goal set")
        ttk.Label(goal_frame, textvariable=self.goal_var).pack(side="left", padx=(0, 10))
        self.goal_entry_var = tk.StringVar()
        ttk.Entry(goal_frame, textvariable=self.goal_entry_var, width=10).pack(side="left", padx=4)
        ttk.Button(goal_frame, text="Set Goal", command=self.set_savings_goal).pack(side="left", padx=4)
        self.progress = ttk.Progressbar(goal_frame, length=300, mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True, padx=10)
        # --- Charts area ---
        charts = ttk.Frame(self.dashboard_tab)
        charts.pack(fill="both", expand=True)
        pie_frame = ttk.LabelFrame(charts, text="Expense Distribution by Category", padding=5)
        pie_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        line_frame = ttk.LabelFrame(charts, text="Monthly Expenses vs Savings", padding=5)
        line_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self.pie_container = pie_frame
        self.line_container = line_frame
        self._pie_canvas = None
        self._line_canvas = None