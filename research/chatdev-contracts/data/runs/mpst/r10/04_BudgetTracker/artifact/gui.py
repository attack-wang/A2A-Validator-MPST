    def _refresh_dashboard(self):
        total_expenses, total_savings = self.db.get_totals()
        self.total_expenses_var.set(f"${total_expenses:,.2f}")
        self.total_savings_var.set(f"${total_savings:,.2f}")
        self.net_balance_var.set(f"${total_savings - total_expenses:,.2f}")
        # Savings goal progress
        goal = self.db.get_savings_goal()
        if goal and goal > 0:
            pct = min(total_savings / goal * 100, 100)
            self.progress.configure(maximum=goal, value=min(total_savings, goal))
            self.goal_var.set(f"Goal: ${goal:,.2f} — {pct:.0f}% reached")
        else:
            self.progress.configure(value=0)
            self.goal_var.set("No goal set")
        # Rebuild pie chart (charts module clears its container first)
        category_totals = self.db.get_category_totals()
        labels = [row[0] for row in category_totals]
        values = [row[1] for row in category_totals]
        self._pie_canvas = create_pie_chart(self.pie_container, labels, values)
        # Rebuild line chart (charts module clears its container first)
        monthly_expenses = dict(self.db.get_monthly_expenses())
        monthly_savings = dict(self.db.get_monthly_savings())
        months = sorted(set(monthly_expenses) | set(monthly_savings))
        expense_values = [monthly_expenses.get(m, 0.0) for m in months]
        saving_values = [monthly_savings.get(m, 0.0) for m in months]
        self._line_canvas = create_line_chart(self.line_container, months,
                                              expense_values, saving_values)