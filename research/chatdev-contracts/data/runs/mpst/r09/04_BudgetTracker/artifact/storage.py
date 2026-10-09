'''
storage.py
Persistence layer for the Budget Tracker application.
``DataStorage`` reads and writes the application's data as a single
JSON document inside a dedicated data directory. The document holds
two collections:
* ``transactions`` -- a list of serialized :class:`models.Transaction`.
* ``budgets``      -- a list of serialized :class:`models.Budget`.
Writes are atomic-ish: data is first dumped to a temporary file which
then replaces the real file, reducing the chance of corruption if the
process is interrupted mid-save.
'''
import json
import os
from models import Transaction, Budget
class DataStorage:
    """Loads and saves transactions and budgets as JSON on disk."""
    def __init__(self, data_dir="budget_data", filename="budget_data.json"):
        self.data_dir = data_dir
        self.filepath = os.path.join(data_dir, filename)
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _ensure_dir(self):
        """Create the data directory when it does not exist yet."""
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
    def _read_document(self):
        """Read the whole JSON document, tolerating a missing file."""
        if not os.path.isfile(self.filepath):
            return {"transactions": [], "budgets": []}
        try:
            with open(self.filepath, "r", encoding="utf-8") as handle:
                document = json.load(handle)
        except (json.JSONDecodeError, OSError):
            # Corrupt or unreadable file: start from an empty document
            # rather than crashing the application.
            return {"transactions": [], "budgets": []}
        if not isinstance(document, dict):
            return {"transactions": [], "budgets": []}
        document.setdefault("transactions", [])
        document.setdefault("budgets", [])
        return document
    def _write_document(self, document):
        """Write the whole JSON document to disk safely."""
        self._ensure_dir()
        temp_path = self.filepath + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2)
        os.replace(temp_path, self.filepath)
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def load_transactions(self):
        """Return every stored transaction as ``Transaction`` objects."""
        document = self._read_document()
        transactions = []
        for raw in document["transactions"]:
            try:
                transactions.append(Transaction.from_dict(raw))
            except (ValueError, TypeError):
                # Skip malformed records instead of failing the load.
                continue
        return transactions
    def save_transactions(self, transactions):
        """Persist a list of ``Transaction`` objects."""
        document = self._read_document()
        document["transactions"] = [t.to_dict() for t in transactions]
        self._write_document(document)
    def load_budgets(self):
        """Return every stored budget as ``Budget`` objects."""
        document = self._read_document()
        budgets = []
        for raw in document["budgets"]:
            try:
                budgets.append(Budget.from_dict(raw))
            except (ValueError, TypeError):
                continue
        return budgets
    def save_budgets(self, budgets):
        """Persist a list of ``Budget`` objects."""
        document = self._read_document()
        document["budgets"] = [b.to_dict() for b in budgets]
        self._write_document(document)