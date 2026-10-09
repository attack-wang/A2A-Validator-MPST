import json
import os
from budget import BudgetTracker, Transaction

DEFAULT_FILE = "budget_data.json"


def load(path=DEFAULT_FILE):
    tracker = BudgetTracker()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                tracker.transactions = [Transaction.from_dict(d) for d in data.get("transactions", [])]
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError, AttributeError):
            tracker = BudgetTracker()
    return tracker


def save(tracker, path=DEFAULT_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"transactions": [t.to_dict() for t in tracker.transactions]}, f, indent=2)