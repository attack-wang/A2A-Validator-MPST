'''
reports.py
Builds human-readable text reports: monthly summaries, category
breakdowns, budget status, and savings goal progress.
'''
from datetime import datetime
class ReportGenerator:
    """Produces formatted text reports from BudgetTracker data."""
    def __init__(self, tracker):
        """Store the tracker whose data the reports describe."""
        self.tracker = tracker
    def overall_summary(self):
        """Print all-time income, expenses, net savings, and counts."""
        income = self.tracker.total_income()
        expenses = self.tracker.total_expenses()
        net = self.tracker.net_savings()
        savings_rate = (net / income * 100) if income > 0 else 0.0
        print("\n========== OVERALL SUMMARY ==========")
        print(f"  Total income   : ${income:>12,.2f}")
        print(f"  Total expenses : ${expenses:>12,.2f}")
        print(f"  Net savings    : ${net:>12,.2f}")
        print(f"  Savings rate   : {savings_rate:>11.1f}%")
        print(f"  Transactions   : {len(self.tracker.transactions)}")
        print(f"  Savings goals  : {len(self.tracker.savings_goals)}")
        print(f"  Active budgets : {len(self.tracker.budgets)}")
        print("=====================================")
    def monthly_report(self, month):
        """Print a detailed report for one month ('YYYY-MM')."""
        transactions = self.tracker.get_transactions(month=month)
        income = self.tracker.total_income(month)
        expenses = self.tracker.total_expenses(month)
        print(f"\n========== MONTHLY REPORT: {month} ==========")
        print(f"  Income   : ${income:>12,.2f}")
        print(f"  Expenses : ${expenses:>12,.2f}")
        print(f"  Net      : ${income - expenses:>12,.2f}")
        print(f"  Entries  : {len(transactions)}")
        if transactions:
            print("  " + "-" * 66)
            for t in transactions:
                print(f"  {t}")
        print("=============================================")
    def category_report(self, month=None):
        """Print expense totals per category with percentage share."""
        totals = self.tracker.category_totals(month=month)
        label = month if month else "All time"
        print(f"\n===== CATEGORY BREAKDOWN ({label}) =====")
        if not totals:
            print("  No expense data available.")
            return
        total = sum(totals.values())
        for cat, amount in totals.items():
            pct = amount / total * 100 if total else 0.0
            print(f"  {cat:<18} ${amount:>10,.2f}  ({pct:5.1f}%)")
        print(f"  {'TOTAL':<18} ${total:>10,.2f}")
        print("=========================================")
    def budget_report(self, month=None):
        """Print budget vs actual spending for each budgeted category."""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        status = self.tracker.budget_status(month)
        print(f"\n===== BUDGET STATUS ({month}) =====")
        if not status:
            print("  No budgets configured. Use 'Set Monthly Budget' first.")
            return
        for s in status:
            flag = "  ** OVER BUDGET **" if s["over"] else ""
            print(f"  {s['category']:<18} Spent ${s['spent']:>9,.2f} of ${s['limit']:>9,.2f}"
                  f"  ({s['percent']:5.1f}%){flag}")
        print("====================================")
    def savings_report(self):
        """Print progress for every savings goal."""
        goals = self.tracker.savings_goals
        print("\n===== SAVINGS GOALS =====")
        if not goals:
            print("  No savings goals defined yet.")
            return
        for g in goals:
            deadline = f" (deadline {g.deadline})" if g.deadline else ""
            print(f"  {g.name}{deadline}")
            print(f"    ${g.current_amount:,.2f} of ${g.target_amount:,.2f} saved "
                  f"- ${g.remaining:,.2f} to go")
            print(f"    {self._progress(g.progress_percent)}")
            if g.progress_percent >= 100:
                print("    *** GOAL REACHED! ***")
        print("=========================")
    @staticmethod
    def _progress(percent, width=30):
        """Text progress bar used inside the savings report."""
        percent = max(0.0, min(100.0, percent))
        filled = int(round(width * percent / 100.0))
        return "[" + "#" * filled + "-" * (width - filled) + f"] {percent:5.1f}%"