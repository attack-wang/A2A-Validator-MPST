'''
storage.py
Persistence layer for the Budget Tracker.
JSONStorage saves/loads the entire tracker state (transactions, savings
goals, category budgets) to a single JSON file using an atomic
write-then-replace strategy so a crash never corrupts the data file.
'''
import json
import os
import tempfile
DEFAULT_FILE = "budget_data.json"
class JSONStorage:
    """Load and save tracker state as a JSON file on disk."""
    def __init__(self, filepath: str = DEFAULT_FILE):
        self.filepath = filepath
    def load(self) -> dict:
        """Return the stored state, or an empty state if no file exists."""
        if not os.path.exists(self.filepath):
            return self._empty_state()
        try:
            with open(self.filepath, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            raise RuntimeError(
                f"Could not read data file '{self.filepath}': {exc}"
            ) from exc
        if not isinstance(raw, dict):
            raise RuntimeError(
                f"Data file '{self.filepath}' is corrupted (not a JSON object)."
            )
        state = self._empty_state()
        state["transactions"] = raw.get("transactions", []) or []
        state["goals"] = raw.get("goals", []) or []
        state["category_budgets"] = raw.get("category_budgets", []) or []
        return state
    def save(self, state: dict) -> None:
        """Atomically write *state* to the JSON file."""
        directory = os.path.dirname(os.path.abspath(self.filepath))
        os.makedirs(directory, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(
            prefix="budget_", suffix=".tmp", dir=directory
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
                json.dump(state, fh, indent=2, ensure_ascii=False)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_path, self.filepath)
        except (OSError, TypeError, ValueError) as exc:
            # Clean up the temporary file so a failed save leaves no litter.
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise RuntimeError(
                f"Could not save data to '{self.filepath}': {exc}"
            ) from exc
    @staticmethod
    def _empty_state() -> dict:
        """Return a fresh, empty tracker state dictionary."""
        return {
            "transactions": [],
            "goals": [],
            "category_budgets": [],
        }