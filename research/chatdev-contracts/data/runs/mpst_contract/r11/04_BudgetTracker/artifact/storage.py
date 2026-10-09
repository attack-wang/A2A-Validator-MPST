import json
import os

DATA_FILE = os.path.join(os.path.expanduser("~"), ".budget_tracker.json")


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                data.setdefault("transactions", [])
                data.setdefault("goals", [])
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {"transactions": [], "goals": []}


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        print(f"Warning: could not save data ({e})")