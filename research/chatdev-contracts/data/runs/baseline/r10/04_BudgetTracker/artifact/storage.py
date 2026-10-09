'''
storage.py
Persistence layer for the Budget Tracker.
Provides JSONStorage, which loads/saves the tracker data as JSON with:
  * atomic writes (write to a temp file, then os.replace)
  * corruption recovery (backs up unreadable files instead of crashing)
'''
import copy
import json
import os
import shutil
from datetime import datetime
EMPTY_DATA = {"expenses": [], "savings_goals": []}
class JSONStorage:
    """Reads and writes tracker data as a JSON file."""
    def __init__(self, filepath="budget_data.json"):
        self.filepath = filepath
    def load(self):
        """Return tracker data; recover gracefully from a corrupt file."""
        if not os.path.exists(self.filepath):
            return copy.deepcopy(EMPTY_DATA)
        try:
            with open(self.filepath, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_path = f"{self.filepath}.corrupt-{timestamp}.bak"
            try:
                shutil.copy2(self.filepath, backup_path)
                print(f"WARNING: data file was corrupted; backed up to {backup_path}")
            except OSError:
                print("WARNING: data file was corrupted and could not be backed up.")
            return copy.deepcopy(EMPTY_DATA)
        if not isinstance(data, dict):
            return copy.deepcopy(EMPTY_DATA)
        data.setdefault("expenses", [])
        data.setdefault("savings_goals", [])
        return data
    def save(self, data):
        """Atomically write tracker data to disk."""
        tmp_path = self.filepath + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self.filepath)
        except OSError as exc:
            raise OSError(f"Could not save data to {self.filepath}: {exc}")