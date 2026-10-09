'''
reports.py
Builds human-readable text reports (monthly summaries, category
breakdowns, budget status, savings progress) from tracker data.
'''
from datetime import datetime
class ReportGenerator:
    """Produces formatted text reports from a BudgetTracker instance."""
    WIDTH = 52
    def __init__(self, tracker):
        self.tracker = tracker
    def _header(self, title):
        """Build a centered section header."""
        lines = ["=" * self.WIDTH]
        lines.append(title.center(self.WIDTH))
        lines.append("=" * self.WIDTH)
        return lines
    def monthly_summary(self, year, month):
        """Return a formatted income/expense/savings summary for a month."""
        summary = self.tracker.monthly_summary(year, month)
        lines = self._header(f"MONTHLY SUMMARY - {datetime(year, month, 1):%B %Y}")
        lines.append(f"  Total Income  : ${summary['income']:>12,.2f}")
        lines.append(f"  Total Expenses: ${summary['expenses']:>12,.2f}")
        lines.append(f"  To Savings    : ${summary['savings']:>12,.2f}")
        lines.append("-" * self.WIDTH)
        lines.append(f"  Net (kept)    : ${summary['net']:>12,.2f}")
        lines.append("=" * self.WIDTH)
        return "\n".join(lines)
    def category_breakdown(self, year, month):
        """Return a formatted breakdown of expenses per category."""
        breakdown = self.tracker.category_breakdown(year, month)
        total = sum(breakdown.values())
        lines = self._header(f"EXPENSES BY CATEGORY - {datetime(year, month, 1):%B %Y}")
        if not breakdown:
            lines.append("  No expenses recorded for this month.")
        else:
            for category, amount in sorted(breakdown.items(),
                                           key=lambda kv: kv[1], reverse=True):
                pct = (amount / total * 100.0) if total else 0.0
                bar = "#" * int(round(pct / 5))
                lines.append(f"  {category:<18} ${amount:>10,.2f}  {pct:5.1f}%  {bar}")
        lines.append("=" * self.WIDTH)
        return "\n".join(lines)
    def budget_report(self, year, month):
        """Return a formatted budget-vs-actual status table."""
        lines = self._header(f"BUDGET STATUS - {datetime(year, month, 1):%B %Y}")
        budgets = self.tracker.budgets
        if not budgets:
            lines.append("  No budgets defined. Add one from the main menu.")
        else:
            lines.append(f"  {'Category':<18} {'Limit':>11} {'Spent':>11} "
                         f"{'Left':>11}  Status")
            lines.append("-" * self.WIDTH)
            for b in sorted(budgets, key=lambda x: x.category):
                spent = b.spent(self.tracker.transactions, year, month)
                left = b.remaining(self.tracker.transactions, year, month)
                status = b.status_symbol(self.tracker.transactions, year, month)
                lines.append(f"  {b.category:<18} ${b.monthly_limit:>10,.2f} "
                             f"${spent:>10,.2f} ${left:>10,.2f}  [{status}]")
        lines.append("=" * self.WIDTH)
        return "\n".join(lines)
    def savings_report(self):
        """Return a formatted progress report for all savings goals."""
        lines = self._header("SAVINGS GOALS PROGRESS")
        if not self.tracker.goals:
            lines.append("  No savings goals defined yet.")
        else:
            for g in self.tracker.goals:
                lines.append(f"  {g}")
                if not g.is_complete:
                    lines.append(f"  {'':<18} Remaining: ${g.remaining:,.2f}")
        lines.append("=" * self.WIDTH)
        return "\n".join(lines)
    def recent_transactions(self, count=10):
        """Return the most recent transactions, newest first."""
        lines = self._header(f"LAST {count} TRANSACTIONS")
        if not self.tracker.transactions:
            lines.append("  No transactions recorded yet.")
        else:
            for t in list(reversed(self.tracker.transactions))[:count]:
                lines.append(f"  {t}")
        lines.append("=" * self.WIDTH)
        return "\n".join(lines)