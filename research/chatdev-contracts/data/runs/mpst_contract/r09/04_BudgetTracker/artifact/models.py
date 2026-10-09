import uuid
from datetime import datetime


class Transaction:
    def __init__(self, ttype, category, amount, date=None, note=""):
        self.id = uuid.uuid4().hex[:8]
        self.type = ttype
        self.category = category
        self.amount = round(float(amount), 2)
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.note = note

    def to_dict(self):
        return {"id": self.id, "type": self.type, "category": self.category,
                "amount": self.amount, "date": self.date, "note": self.note}

    @classmethod
    def from_dict(cls, data):
        t = cls(data["type"], data["category"], data["amount"],
                data.get("date"), data.get("note", ""))
        t.id = data.get("id", t.id)
        return t


class Budget:
    def __init__(self, category, limit):
        self.category = category
        self.limit = round(float(limit), 2)

    def to_dict(self):
        return {"category": self.category, "limit": self.limit}

    @classmethod
    def from_dict(cls, data):
        return cls(data["category"], data["limit"])