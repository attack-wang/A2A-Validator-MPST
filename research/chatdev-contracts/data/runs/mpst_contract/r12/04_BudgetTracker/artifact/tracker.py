import datetime


class BudgetTracker:
    """Core budget logic: transactions, category reports, and savings goals."""

    def __init__(self, data):
        self.data = data
        if "transactions" not in self.data:
            self.data["transactions"] = []
        if "goals" not in self.data:
            self.data["goals"] = []

    def add_transaction(self, ttype, amount, category, note=""):
        entry = {
            "id": len(self.data["transactions"]) + 1,
            "type": ttype,
            "amount": round(float(amount), 2),
            "category": category,
            "note": note,
            "date": datetime.date.today().isoformat(),
        }
        self.data["transactions"].append(entry)
        return entry

    def transactions(self, ttype=None, month=None):
        result = self.data["transactions"]
        if ttype:
            result = [t for t in result if t["type"] == ttype]
        if month:
            result = [t for t in result if t["date"].startswith(month)]
        return result

    def totals(self, month=None):
        totals = {"income": 0.0, "expense": 0.0, "saving": 0.0}
        for t in self.transactions(month=month):
            totals[t["type"]] += t["amount"]
        totals["balance"] = totals["income"] - totals["expense"]
        totals["net"] = totals["balance"] - totals["saving"]
        return totals

    def by_category(self, ttype="expense", month=None):
        cats = {}
        for t in self.transactions(ttype=ttype, month=month):
            cats[t["category"]] = cats.get(t["category"], 0.0) + t["amount"]
        return dict(sorted(cats.items(), key=lambda kv: kv[1], reverse=True))

    def add_goal(self, name, target):
        goal = {"name": name, "target": round(float(target), 2), "saved": 0.0}
        self.data["goals"].append(goal)
        return goal

    def contribute_goal(self, index, amount):
        goal = self.data["goals"][index]
        room = max(goal["target"] - goal["saved"], 0.0)
        added = round(min(float(amount), room), 2)
        goal["saved"] = round(goal["saved"] + added, 2)
        return goal, added

    def goals_report(self):
        lines = []
        for i, g in enumerate(self.data["goals"]):
            pct = (g["saved"] / g["target"] * 100) if g["target"] > 0 else 100.0
            bar = "#" * int(pct // 5)
            status = " (complete)" if g["saved"] >= g["target"] else ""
            lines.append(
                f"[{i}] {g['name']}: ${g['saved']:.2f} / ${g['target']:.2f}"
                f" ({pct:.0f}%) {bar}{status}"
            )
        return lines