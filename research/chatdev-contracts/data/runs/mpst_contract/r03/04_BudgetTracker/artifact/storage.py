import json
from tracker import BudgetTracker


class Storage:
    def __init__(self, path):
        self.path = path

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return BudgetTracker.from_dict(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            return BudgetTracker()

    def save(self, tracker):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(tracker.to_dict(), f, indent=2)