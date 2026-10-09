import json
import os
from datetime import datetime

VALID_TYPES = ("expense", "income", "savings")


class BudgetTracker:
    def __init__(self, filepath="budget_data.json"):
        self.filepath = filepath
        self.transactions = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.transactions = data.get("transactions", [])
            except (json.JSONDecodeError, OSError):
                self.transactions = []

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump({"transactions": self.transactions}, f, indent=2)

    def add_transaction(self, ttype, category, amount, note=""):
        if ttype not in VALID_TYPES:
            raise ValueError("Type must be expense, income, or savings.")
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": ttype,
            "category": category.strip() or "Uncategorized",
            "amount": round(amount, 2),
            "note": note.strip(),
        }
        self.transactions.append(entry)
        self.save()
        return entry

    def remove_transaction(self, index):
        if 0 <= index < len(self.transactions):
            removed = self.transactions.pop(index)
            self.save()
            return removed
        raise IndexError("Invalid transaction number.")

    def list_transactions(self):
        return list(self.transactions)

    def summary(self):
        totals = {"expense": 0.0, "income": 0.0, "savings": 0.0}
        for t in self.transactions:
            totals[t["type"]] += t["amount"]
        return {
            "income": round(totals["income"], 2),
            "expenses": round(totals["expense"], 2),
            "savings": round(totals["savings"], 2),
            "balance": round(totals["income"] - totals["expense"], 2),
        }

    def category_breakdown(self):
        breakdown = {}
        for t in self.transactions:
            if t["type"] == "expense":
                breakdown[t["category"]] = breakdown.get(t["category"], 0.0) + t["amount"]
        return {k: round(v, 2) for k, v in sorted(breakdown.items(), key=lambda x: -x[1])}