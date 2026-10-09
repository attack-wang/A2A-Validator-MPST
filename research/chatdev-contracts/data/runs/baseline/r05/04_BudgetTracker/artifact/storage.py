'''
storage.py
Persistence layer for the Budget Tracker application.
Provides the Storage class, which saves and loads all application data
(transactions, budgets, savings goals) as a single JSON file so the
customer's records carry across sessions.
'''
import json
import os
DEFAULT_FILENAME = "budget_data.json"
class Storage:
    """Handles reading and writing budget data to a JSON file on disk."""
    def __init__(self, filepath=None):
        """Accept an optional filepath; default to budget_data.json in cwd."""
        self.filepath = filepath or DEFAULT_FILENAME
    def exists(self):
        """Return True if the data file already exists."""
        return os.path.exists(self.filepath)
    def save(self, data):
        """Write the given dictionary to disk as JSON."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
            return True
        except (OSError, TypeError) as exc:
            print(f"[Storage] Failed to save data: {exc}")
            return False
    def load(self):
        """Read the JSON data file; return None if missing or corrupted."""
        if not self.exists():
            return None
        try:
            with open(self.filepath, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[Storage] Failed to load data: {exc}")
            return None