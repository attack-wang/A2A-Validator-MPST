"""
storage.py
Persistence layer for the Budget Tracker application.
Provides the Storage class, which handles reading and writing all
application data (expenses, savings goals, settings) to a JSON file
on disk. Data is loaded eagerly and saved atomically (write to a
temporary file, then replace) to avoid corrupting the data file.
"""
import json
import os
import tempfile
from typing import Any, Dict
DEFAULT_DATA_FILE = "budget_data.json"
class Storage:
    """Handles loading and saving application data as JSON."""
    def __init__(self, filepath: str = DEFAULT_DATA_FILE):
        self.filepath = filepath
    def load(self) -> Dict[str, Any]:
        """Load data from the JSON file; return defaults if missing/corrupt."""
        default = {"expenses": [], "savings_goals": [], "settings": {"monthly_budget": 0.0}}
        if not os.path.exists(self.filepath):
            return default
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Corrupt or unreadable file: fall back to defaults rather than crash
            return default
        # Ensure all expected keys exist
        data.setdefault("expenses", [])
        data.setdefault("savings_goals", [])
        settings = data.setdefault("settings", {})
        settings.setdefault("monthly_budget", 0.0)
        return data
    def save(self, data: Dict[str, Any]) -> None:
        """Save data to the JSON file atomically."""
        directory = os.path.dirname(os.path.abspath(self.filepath))
        os.makedirs(directory, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_path, self.filepath)
        except OSError:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise