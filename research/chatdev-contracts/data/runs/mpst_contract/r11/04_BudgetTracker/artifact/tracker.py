import datetime


class BudgetTracker:
    def __init__(self, data):
        self.data = data

    def add_transaction(self, ttype, category, amount, note=""):
        self.data["transactions"].append({
            "type": ttype,
            "category": category,
            "amount": round(amount, 2),
            "note": note,
            "date": datetime.date.today().isoformat(),
        })

    def remove_transaction(self, index):
        txs = self.data["transactions"]
        if 0 <= index < len(txs):
            return txs.pop(index)
        return None

    def transactions(self):
        return self.data["transactions"]

    def totals(self):
        income = sum(t["amount"] for t in self.data["transactions"]
                     if t["type"] == "income")
        expenses = sum(t["amount"] for t in self.data["transactions"]
                       if t["type"] == "expense")
        return income, expenses, income - expenses

    def by_category(self):
        cats = {}
        for t in self.data["transactions"]:
            if t["type"] == "expense":
                cats[t["category"]] = cats.get(t["category"], 0.0) + t["amount"]
        return cats

    def add_goal(self, name, target):
        self.data["goals"].append(
            {"name": name, "target": round(target, 2), "saved": 0.0})

    def contribute_goal(self, index, amount):
        goals = self.data["goals"]
        if 0 <= index < len(goals):
            g = goals[index]
            g["saved"] = round(min(g["target"], g["saved"] + amount), 2)
            return True
        return False

    def goals(self):
        return self.data["goals"]