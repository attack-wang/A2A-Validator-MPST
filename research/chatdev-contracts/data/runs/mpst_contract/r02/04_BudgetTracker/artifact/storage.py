import json
import os

DATA_FILE = "budget_data.json"

EMPTY_DATA = {"transactions": [], "budgets": {}, "savings_goal": 0.0}


def load_data(path=DATA_FILE):
    if not os.path.exists(path):
        return dict(EMPTY_DATA)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return dict(EMPTY_DATA)
    data.setdefault("transactions", [])
    data.setdefault("budgets", {})
    data.setdefault("savings_goal", 0.0)
    return data


def save_data(data, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)