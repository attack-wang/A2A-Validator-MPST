'''
storage.py
Persistence layer for the Budget Tracker application.
Classes:
    JSONStorage: Loads and saves all budget data (transactions and budgets)
        as a single JSON document on disk.
'''
import json
import os
class JSONStorage:
    """Handles reading and writing budget data to a JSON file."""
    DEFAULT_FILENAME = "budget_data.json"
    def __init__(self, filepath=None):
        """
        Initialize the storage handler.
        Args:
            filepath (str, optional): Path of the JSON data file.
                Defaults to 'budget_data.json' next to this module.
        """
        if filepath is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(base_dir, self.DEFAULT_FILENAME)
        self.filepath = filepath
    def load(self):
        """
        Load and return the stored data.
        Returns:
            dict: {'transactions': [dict, ...], 'budgets': {category: amount}}
                Returns an empty structure when the file is missing or
                corrupted so the application can still start cleanly.
        """
        empty = {"transactions": [], "budgets": {}}
        if not os.path.exists(self.filepath):
            return empty
        try:
            with open(self.filepath, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return empty
        if not isinstance(data, dict):
            return empty
        data.setdefault("transactions", [])
        data.setdefault("budgets", {})
        if not isinstance(data["transactions"], list):
            data["transactions"] = []
        if not isinstance(data["budgets"], dict):
            data["budgets"] = {}
        return data
    def save(self, data):
        """
        Persist the given data structure to disk.
        Args:
            data (dict): {'transactions': [...], 'budgets': {...}}
        """
        try:
            with open(self.filepath, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
        except OSError as exc:
            raise IOError(f"Could not save budget data: {exc}")