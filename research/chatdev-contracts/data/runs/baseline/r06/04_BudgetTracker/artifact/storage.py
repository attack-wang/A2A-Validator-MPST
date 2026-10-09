'''
storage.py
Persistence layer for the budget tracker. Saves/loads all application
data (expenses, savings goals, budget settings) to/from a JSON file.
'''
import json
import os
import shutil
from datetime import datetime
from models import Transaction, SavingsGoal, Budget
class StorageManager:
    """Handles loading and saving of budget data as a JSON file."""
    DEFAULT_FILENAME = "budget_data.json"
    def __init__(self, filename=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(base_dir, filename or self.DEFAULT_FILENAME)
    def load(self):
        """
        Load and return (transactions, goals, budget).
        Returns empty data structures when the file does not exist. If the
        file is corrupted, it is backed up and fresh data is returned so the
        application can still start.
        """
        if not os.path.exists(self.filepath):
            return [], [], Budget()
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Back up the corrupted file and start fresh.
            self._backup_corrupted()
            return [], [], Budget()
        if not isinstance(raw, dict):
            self._backup_corrupted()
            return [], [], Budget()
        transactions = []
        for entry in raw.get("expenses", []):
            try:
                transactions.append(Transaction.from_dict(entry))
            except (ValueError, TypeError):
                continue  # Skip malformed entries instead of failing the load.
        goals = []
        for entry in raw.get("goals", []):
            try:
                goals.append(SavingsGoal.from_dict(entry))
            except (ValueError, TypeError):
                continue
        try:
            budget = Budget.from_dict(raw.get("budget", {}))
        except (ValueError, TypeError):
            budget = Budget()
        return transactions, goals, budget
    def save(self, transactions, goals, budget):
        """
        Persist transactions, savings goals and budget settings to disk.
        Raises IOError when the file cannot be written so the caller (GUI)
        can show a friendly error message.
        """
        data = {
            "expenses": [t.to_dict() for t in transactions],
            "goals": [g.to_dict() for g in goals],
            "budget": budget.to_dict(),
            "saved_at": datetime.now().isoformat(timespec="seconds"),
        }
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise IOError(f"Could not save budget data to {self.filepath}: {exc}") from exc
    def _backup_corrupted(self):
        """Copy the current (corrupted) data file to a timestamped backup."""
        backup = self.filepath + ".bak-" + datetime.now().strftime("%Y%m%d%H%M%S")
        try:
            shutil.copy2(self.filepath, backup)
        except OSError:
            pass
    def backup(self):
        """Create a timestamped manual backup. Returns the backup path or None."""
        if not os.path.exists(self.filepath):
            return None
        backup = self.filepath + ".bak-" + datetime.now().strftime("%Y%m%d%H%M%S")
        try:
            shutil.copy2(self.filepath, backup)
            return backup
        except OSError:
            return None
    def clear(self):
        """Delete the data file so the application starts fresh."""
        try:
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
        except OSError:
            pass