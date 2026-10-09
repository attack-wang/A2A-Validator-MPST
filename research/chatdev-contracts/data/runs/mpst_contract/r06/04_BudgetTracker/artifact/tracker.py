import datetime
from models import Transaction
import storage

KINDS = ("expense", "income", "savings")


class BudgetTracker:
    def __init__(self):
        self.data = storage.load_data()

    def _save(self):
        storage.save_data(self.data)

    def add(self, kind, category, description, amount, date=None):
        if kind not in KINDS:
            raise ValueError("Type must be expense, income, or savings.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        date = date or datetime.date.today().isoformat()
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")
        t = Transaction(self.data["next_id"], date, kind, category or "General",
                        description or "", round(float(amount), 2))
        self.data["next_id"] += 1
        self.data["transactions"].append(t.to_dict())
        self._save()
        return t

    def delete(self, tid):
        before = len(self.data["transactions"])
        self.data["transactions"] = [t for t in self.data["transactions"] if int(t["id"]) != tid]
        if len(self.data["transactions"]) == before:
            raise ValueError("Transaction not found.")
        self._save()

    def list_all(self):
        return sorted((Transaction.from_dict(t) for t in self.data["transactions"]),
                      key=lambda t: (t.date, t.id))

    def summary(self):
        inc = exp = sav = 0.0
        for t in self.data["transactions"]:
            a = float(t["amount"])
            if t["kind"] == "income":
                inc += a
            elif t["kind"] == "expense":
                exp += a
            else:
                sav += a
        return {"income": inc, "expenses": exp, "savings": sav, "balance": inc - exp - sav}

    def by_category(self, kind="expense"):
        cats = {}
        for t in self.data["transactions"]:
            if t["kind"] == kind:
                cats[t["category"]] = cats.get(t["category"], 0.0) + float(t["amount"])
        return dict(sorted(cats.items(), key=lambda kv: -kv[1]))

    def monthly(self, month=None):
        month = month or datetime.date.today().strftime("%Y-%m")
        try:
            month = datetime.datetime.strptime(month, "%Y-%m").strftime("%Y-%m")
        except ValueError:
            raise ValueError("Month must be in YYYY-MM format.")
        inc = exp = sav = 0.0
        for t in self.data["transactions"]:
            if str(t["date"])[:7] == month:
                a = float(t["amount"])
                if t["kind"] == "income":
                    inc += a
                elif t["kind"] == "expense":
                    exp += a
                else:
                    sav += a
        return {"month": month, "income": inc, "expenses": exp,
                "savings": sav, "balance": inc - exp - sav}