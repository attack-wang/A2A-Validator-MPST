'''
visualizer.py
Chart generation for the budget tracker using matplotlib.
Falls back to text-based summaries when matplotlib is unavailable.
'''
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
class Visualizer:
    """Creates matplotlib figures (or text fallbacks) for budget data."""
    def __init__(self, tracker):
        self.tracker = tracker
    # ---- Matplotlib figures ----
    def expense_pie_figure(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        data = self.tracker.expenses_by_category()
        if not data:
            ax.text(0.5, 0.5, "No expense data", ha="center", va="center")
            return fig
        labels = list(data.keys())
        values = list(data.values())
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Expenses by Category")
        ax.axis("equal")
        return fig
    def expense_trend_figure(self):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        monthly = self.tracker.monthly_expenses()
        if not monthly:
            ax.text(0.5, 0.5, "No expense data", ha="center", va="center")
            return fig
        months = list(monthly.keys())
        totals = list(monthly.values())
        ax.plot(months, totals, marker="o")
        ax.set_title("Monthly Expense Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Spent")
        ax.grid(True, alpha=0.3)
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_ha("right")
        return fig
    def savings_progress_figure(self):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        goals = self.tracker.savings_goals
        if not goals:
            ax.text(0.5, 0.5, "No savings goals", ha="center", va="center")
            return fig
        names = [g.name for g in goals]
        saved = [g.saved_amount for g in goals]
        targets = [g.target_amount for g in goals]
        y = range(len(goals))
        ax.barh(y, targets, color="#dddddd", label="Target")
        ax.barh(y, saved, color="#4CAF50", label="Saved")
        ax.set_yticks(list(y))
        ax.set_yticklabels(names)
        ax.set_title("Savings Progress")
        ax.legend()
        return fig
    # ---- Text fallbacks (used when matplotlib is unavailable) ----
    def expense_pie_text(self):
        data = self.tracker.expenses_by_category()
        total = sum(data.values())
        lines = ["Expense Breakdown by Category", "=" * 30]
        if not data:
            lines.append("(no expenses recorded)")
            return "\n".join(lines)
        for cat, val in sorted(data.items(), key=lambda kv: kv[1], reverse=True):
            pct = val / total * 100 if total else 0
            bar = "#" * int(pct / 2)
            lines.append(f"{cat:<15} {val:>10.2f} ({pct:5.1f}%) {bar}")
        return "\n".join(lines)
    def text_summary(self):
        lines = []
        lines.append("=== Budget Summary ===")
        lines.append(f"Total expenses: {self.tracker.total_expenses():.2f}")
        lines.append(f"Total saved:    {self.tracker.total_saved():.2f}")
        lines.append("")
        lines.append(self.expense_pie_text())
        return "\n".join(lines)