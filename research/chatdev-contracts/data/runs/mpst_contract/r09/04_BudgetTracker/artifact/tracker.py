import storage
from datetime import datetime
from models import Transaction, Budget


class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.budgets = {}

    def load(self):
        data = storage.load_data()
        self.transactions = [Transaction.from_dict(d) for d in data["transactions"]]
        self.budgets = {d["category"]: Budget.from_dict(d) for d in data["budgets"]}

    def save(self):
        data = {
            "transactions": [t.to_dict() for t in self.transactions],
            "budgets": [b.to_dict() for b in self.budgets.values()],
        }
        storage.save_data(data)

    def add_transaction(self, ttype, category, amount, date=None, note=""):
        t = Transaction(ttype, category, amount, date, note)
        self.transactions.append(t)
        self.save()
        return t

    def remove_transaction(self, tid):
        before = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.id != tid]
        if len(self.transactions) != before:
            self.save()
            return True
        return False

    def set_budget(self, category, limit):
        self.budgets[category] = Budget(category, limit)
        self.save()

    def total(self, ttype):
        return round(sum(t.amount for t in self.transactions if t.type == ttype), 2)

    def savings(self):
        return round(self.total("income") - self.total("expense"), 2)

    def spent_by_category(self, month=None):
        spent = {}
        for t in self.transactions:
            if t.type == "expense" and (month is None or t.date.startswith(month)):
                spent[t.category] = round(spent.get(t.category, 0.0) + t.amount, 2)
        return spent

    def budget_status(self):
        current_month = datetime.now().strftime("%Y-%m")
        spent = self.spent_by_category(current_month)
        return [(b.category, b.limit, spent.get(b.category, 0.0))
                for b in self.budgets.values()]