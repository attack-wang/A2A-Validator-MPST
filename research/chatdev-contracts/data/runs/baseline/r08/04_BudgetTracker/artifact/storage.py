'''
storage.py
JSON-file persistence layer for the Budget Tracker.
'''
import json
import os
DEFAULT_DATA_FILE = "budget_data.json"
class JSONStorage:
    """Loads and saves the budget data as a JSON document on disk."""
    def __init__(self, filepath=DEFAULT_DATA_FILE):
        self.filepath = filepath
    def load(self):
        """Return (transactions_dicts, goals_dicts); empty lists if no file."""
        if not os.path.exists(self.filepath):
            return [], []
        try:
            with open(self.filepath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data.get("transactions", []), data.get("goals", [])
        except (json.JSONDecodeError, OSError):
            return [], []
    def save(self, transactions, goals):
        data = {
            "transactions": [t.to_dict() for t in transactions],
            "goals": [g.to_dict() for g in goals],
        }
        with open(self.filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)