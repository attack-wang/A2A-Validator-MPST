'''
storage.py
Handles persistence of all Budget Tracker data (transactions, savings goals,
budgets) in a single JSON file. Provides atomic-ish save and safe load with
sensible defaults for missing or corrupted files.
'''
import json
import os
import tempfile
DATA_FILE = "budget_data.json"
class DataStorage:
    """Loads and saves the application's data dictionary to a JSON file."""
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
    def load(self):
        """Return the stored data as a dict, or a fresh default structure."""
        default = {"transactions": [], "savings_goals": [], "budgets": []}
        if not os.path.exists(self.filepath):
            return default
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Corrupted or unreadable file: back it up and start fresh.
            try:
                os.rename(self.filepath, self.filepath + ".corrupt")
            except OSError:
                pass
            return default
        if not isinstance(data, dict):
            # Unexpected top-level structure: back it up and start fresh.
            try:
                os.rename(self.filepath, self.filepath + ".corrupt")
            except OSError:
                pass
            return default
        # Guarantee all keys exist even if the file was hand-edited.
        for key in default:
            data.setdefault(key, [])
        # Keep only well-formed entries so model.from_dict never crashes.
        for key in default:
            data[key] = [item for item in data[key] if isinstance(item, dict)]
        return data
    def save(self, data):
        """Persist the data dictionary to disk as pretty-printed JSON."""
        directory = os.path.dirname(os.path.abspath(self.filepath)) or "."
        tmp_path = None
        try:
            # Write to a temporary file first, then atomically replace the
            # target file so an interrupted write never corrupts the data.
            fd, tmp_path = tempfile.mkstemp(prefix=".budget_tmp_", dir=directory)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self.filepath)
            tmp_path = None
        except OSError:
            # Fallback: direct write if atomic replacement is unavailable.
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass