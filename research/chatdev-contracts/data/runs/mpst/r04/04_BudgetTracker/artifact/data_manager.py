'''
data_manager.py
Handles loading and saving of all budget tracker data (transactions,
budgets, savings goals) as a single JSON file on disk.
'''
import json
import os
class DataManager:
    """Reads/writes the tracker's persistent state to a JSON file."""
    def __init__(self, filepath="budget_data.json"):
        self.filepath = filepath
    def load(self):
        """Return the raw data dictionary, or an empty structure if no file."""
        if not os.path.exists(self.filepath):
            return {"transactions": [], "budgets": [], "goals": []}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Corrupt or unreadable file: start fresh rather than crash.
            return {"transactions": [], "budgets": [], "goals": []}
        data.setdefault("transactions", [])
        data.setdefault("budgets", [])
        data.setdefault("goals", [])
        return data
    def save(self, data):
        """Persist the data dictionary to disk (atomic via temp file)."""
        tmp = self.filepath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, self.filepath)