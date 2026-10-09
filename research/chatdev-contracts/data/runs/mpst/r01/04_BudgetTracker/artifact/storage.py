'''
storage.py
Persistence layer for the Budget Tracker application.
Stores all application data (transactions, budgets, savings goals)
as a single JSON file on disk. Writes are atomic (via a temporary
file + os.replace) to prevent data corruption.
'''
import json
import os
DEFAULT_FILENAME = "budget_data.json"
class Storage:
    """Handles loading and saving application data as JSON."""
    def __init__(self, filepath=None):
        self.filepath = filepath if filepath else DEFAULT_FILENAME
    def load(self):
        """Load data from disk. Returns an empty dict if no file exists."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # Corrupt or unreadable file: start fresh rather than crash.
            return {}
    def save(self, data):
        """Persist the given data dict to disk as JSON (atomically)."""
        temp_path = self.filepath + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, self.filepath)