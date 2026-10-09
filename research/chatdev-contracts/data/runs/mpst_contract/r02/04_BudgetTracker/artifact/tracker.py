from datetime import datetime

from models import Transaction


class BudgetTracker:
    def __init__(self, data):
        self.data = data
        self.transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
        self.budgets = dict(data.get("budgets", {}))
        self.savings_goal = float(data.get("savings_goal", 0.0))

    def persist(self):
        self.data["transactions"] = [t.to_dict() for t in self.transactions]
        self.data["budgets"] = self.budgets
        self.data["savings_goal"] = self.savings_goal
        return self.data

    def add_transaction(self, amount, category, tx_type, note=""):
        tx = Transaction(round(amount, 2), category, tx_type, note)
        self.transactions.append(tx)
        return tx

    def remove_transaction(self, tx_id):
        before = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.id != tx_id]
        return len(self.transactions) < before

    def set_budget(self, category, limit):
        self.budgets[category] = round(limit, 2)

    def set_savings_goal(self, goal):
        self.savings_goal = round(goal, 2)

    def totals(self):
        income = sum(t.amount for t in self.transactions if t.tx_type == "income")
        expenses = sum(t.amount for t in self.transactions if t.tx_type == "expense")
        return income, expenses, income - expenses

    def category_expenses(self, rows=None):
        cats = {}
        for t in (rows if rows is not None else self.transactions):
            if t.tx_type == "expense":
                cats[t.category] = cats.get(t.category, 0.0) + t.amount
        return cats

    def budget_status(self):
        current_month = datetime.now().strftime("%Y-%m")
        month_rows = [t for t in self.transactions if t.date.startswith(current_month)]
        spent = self.category_expenses(month_rows)
        return {
            cat: {
                "limit": lim,
                "spent": round(spent.get(cat, 0.0), 2),
                "remaining": round(lim - spent.get(cat, 0.0), 2),
            }
            for cat, lim in self.budgets.items()
        }

    def savings_progress(self):
        _, _, net = self.totals()
        pct = (net / self.savings_goal * 100) if self.savings_goal > 0 else 0.0
        return net, self.savings_goal, min(max(pct, 0.0), 100.0)

    def monthly_report(self, month=None):
        rows = [t for t in self.transactions if month is None or t.date.startswith(month)]
        income = sum(t.amount for t in rows if t.tx_type == "income")
        expenses = sum(t.amount for t in rows if t.tx_type == "expense")
        return income, expenses, income - expenses, rows