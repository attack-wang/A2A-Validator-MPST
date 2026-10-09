import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget_data.json")


def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, dict):
                raise ValueError("Corrupt data file.")
            data.setdefault("transactions", [])
            data.setdefault("goals", [])
            data.setdefault("next_id", 1)
            return data
        except (json.JSONDecodeError, ValueError, OSError):
            pass
    return {"transactions": [], "goals": [], "next_id": 1}


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)