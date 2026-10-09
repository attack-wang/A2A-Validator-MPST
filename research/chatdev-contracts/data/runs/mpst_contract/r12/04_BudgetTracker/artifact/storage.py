import json
import os

DATA_FILE = "budget_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {"transactions": [], "goals": []}


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    except OSError as exc:
        print(f"Warning: could not save data ({exc}).")