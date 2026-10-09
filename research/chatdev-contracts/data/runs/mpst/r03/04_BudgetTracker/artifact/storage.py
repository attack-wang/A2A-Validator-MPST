'''
storage.py
Persistence layer for the Budget Tracker application.
Provides the Storage class, which reads and writes all application data
(transactions and budget settings) to a JSON file on disk, so that the
user's financial records survive between sessions.
Key behaviours:
- load(): always returns a well-formed data dictionary. A missing file
  yields sensible defaults; a corrupted or malformed file is first backed
  up with a timestamp suffix so the user never silently loses their
  original data, and then defaults are returned.
- save(): writes atomically (temporary file + os.replace) so an
  interrupted write can never leave a half-written data file behind.
- The directory of the data file is created automatically on save.
'''
import json
import os
import shutil
import tempfile
from datetime import datetime
DEFAULT_DATA_FILE = "budget_data.json"
class Storage:
    """Handles loading and saving of budget data as a JSON document."""
    def __init__(self, filepath=DEFAULT_DATA_FILE):
        """
        Initialize the storage layer.
        Args:
            filepath: Path of the JSON file used to persist all data.
        """
        self.filepath = filepath
    def load(self):
        """
        Load and return the full data dictionary.
        Returns:
            dict: A dictionary containing the keys "transactions" (a list
            of transaction dictionaries) and "monthly_budget" (a float).
            Defaults are returned when the file does not exist, cannot be
            read, is corrupt, or has an unexpected structure.
        """
        default = {"transactions": [], "monthly_budget": 0.0}
        if not os.path.exists(self.filepath):
            return default
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            # Back up the corrupted file so the user does not lose it entirely.
            self._backup_corrupted_file()
            return default
        if not isinstance(data, dict):
            # Unexpected top-level structure: treat as corrupt and back up.
            self._backup_corrupted_file()
            return default
        # Guarantee the expected keys exist with sane, well-typed values.
        transactions = data.get("transactions", [])
        if not isinstance(transactions, list):
            transactions = []
        try:
            monthly_budget = float(data.get("monthly_budget", 0.0))
        except (TypeError, ValueError):
            monthly_budget = 0.0
        return {"transactions": transactions, "monthly_budget": monthly_budget}
    def save(self, data):
        """
        Persist the given data dictionary to disk as JSON.
        The write is performed atomically: the payload is first written to
        a temporary file in the same directory, then moved over the target
        file with os.replace, so a crash mid-write cannot destroy data
        that was previously saved.
        Args:
            data: The dictionary to persist (transactions + settings).
        Raises:
            OSError: If writing to disk fails for any reason.
        """
        directory = os.path.dirname(os.path.abspath(self.filepath))
        os.makedirs(directory, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(
            prefix=os.path.basename(self.filepath) + ".",
            suffix=".tmp",
            dir=directory,
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            # os.replace is atomic on both Windows and POSIX systems.
            os.replace(tmp_path, self.filepath)
        except OSError:
            # Best-effort cleanup of the temporary file on failure.
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise
    def _backup_corrupted_file(self):
        """Copy the current (corrupted) data file to a timestamped backup."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = "{}.backup-{}".format(self.filepath, timestamp)
        try:
            shutil.copy(self.filepath, backup_path)
        except OSError:
            # If even the backup fails there is nothing more we can do;
            # the caller already falls back to the default data set.
            pass