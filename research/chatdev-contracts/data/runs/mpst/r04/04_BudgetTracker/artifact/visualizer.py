'''
visualizer.py
Generates charts for the budget tracker. Uses matplotlib to render
PNG files when available; otherwise falls back to ASCII bar charts
printed to the console.
'''
import os
from datetime import datetime
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
from transaction import Transaction
class Visualizer:
    """Renders charts from tracker data (PNG via matplotlib or ASCII)."""
    def __init__(self, tracker, output_dir="charts"):
        self.tracker = tracker
        self.output_dir = output_dir
        if MATPLOTLIB_AVAILABLE:
            os.makedirs(output_dir, exist_ok=True)
    def expense_pie_chart(self, year, month):
        """Pie chart of expenses by category for a month."""
        breakdown = self.tracker.category_breakdown(year, month)
        if not breakdown:
            return "No expense data for this month - nothing to chart."
        if MATPLOTLIB_AVAILABLE:
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.pie(list(breakdown.values()), labels=list(breakdown.keys()),
                   autopct="%1.1f%%", startangle=90)
            ax.set_title(f"Expenses by Category - {year}-{month:02d}")
            path = os.path.join(self.output_dir, f"expenses_{year}_{month:02d}.png")
            fig.savefig(path, bbox_inches="tight", dpi=150)
            plt.close(fig)
            return f"Pie chart saved to: {path}"
        return self._ascii_bar(breakdown, f"Expenses {year}-{month:02d}")
    def savings_line_chart(self):
        """Line chart of cumulative savings over time."""
        events = sorted(
            (t for t in self.tracker.transactions
             if t.type in (Transaction.TYPE_SAVINGS, Transaction.TYPE_SAVINGS_OUT)),
            key=lambda t: t.date)
        if not events:
            return "No savings activity recorded - nothing to chart."
        cumulative = 0.0
        points, labels = [], []
        for t in events:
            cumulative += t.amount if t.type == Transaction.TYPE_SAVINGS else -t.amount
            points.append(round(cumulative, 2))
            labels.append(t.date)
        if MATPLOTLIB_AVAILABLE:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(labels, points, marker="o", color="tab:green")
            ax.set_title("Cumulative Savings Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Amount ($)")
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            fig.tight_layout()
            path = os.path.join(self.output_dir, "savings_growth.png")
            fig.savefig(path, dpi=150)
            plt.close(fig)
            return f"Line chart saved to: {path}"
        return self._ascii_bar({"Cumulative savings": cumulative},
                               "Cumulative Savings")
    def budget_bar_chart(self, year, month):
        """Bar chart comparing budget limits vs actual spending."""
        if not self.tracker.budgets:
            return "No budgets defined - nothing to chart."
        spent = {b.category: b.spent(self.tracker.transactions, year, month)
                 for b in self.tracker.budgets}
        limits = {b.category: b.monthly_limit for b in self.tracker.budgets}
        if MATPLOTLIB_AVAILABLE:
            cats = list(spent.keys())
            x = range(len(cats))
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.bar([i - 0.2 for i in x], [limits[c] for c in cats],
                   width=0.4, label="Budget limit")
            ax.bar([i + 0.2 for i in x], [spent[c] for c in cats],
                   width=0.4, label="Actual spent")
            ax.set_xticks(list(x))
            ax.set_xticklabels(cats, rotation=30, ha="right")
            ax.set_title(f"Budget vs Spending - {year}-{month:02d}")
            ax.set_ylabel("Amount ($)")
            ax.legend()
            fig.tight_layout()
            path = os.path.join(self.output_dir, f"budget_{year}_{month:02d}.png")
            fig.savefig(path, dpi=150)
            plt.close(fig)
            return f"Bar chart saved to: {path}"
        return self._ascii_bar({c: f"{spent[c]:.2f} / {limits[c]:.2f}" for c in spent},
                               f"Budget vs Spent {year}-{month:02d}")
    def _ascii_bar(self, data_dict, title):
        """Fallback renderer: simple horizontal ASCII bar chart."""
        lines = [title, "-" * 40]
        numeric = [v for v in data_dict.values() if isinstance(v, (int, float))]
        max_val = max(numeric) if numeric else 0
        for key, val in data_dict.items():
            scale = val if isinstance(val, (int, float)) else max_val
            bar = "#" * int(round((scale / max_val) * 30)) if max_val else ""
            lines.append(f"  {str(key):<18} {bar} {val}")
        return "\n".join(lines)