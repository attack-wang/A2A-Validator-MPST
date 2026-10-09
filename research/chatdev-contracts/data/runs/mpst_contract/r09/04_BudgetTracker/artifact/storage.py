import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget_data.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"transactions": [], "budgets": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"transactions": [], "budgets": []}
        data.setdefault("transactions", [])
        data.setdefault("budgets", [])
        return data
    except (json.JSONDecodeError, OSError):
        return {"transactions": [], "budgets": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)