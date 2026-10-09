import json
import os

DATA_FILE = "budget_data.json"

EMPTY_DATA = {
    "transactions": [],
    "budget": {"monthly_income_goal": 0.0, "savings_goal": 0.0, "category_limits": {}},
}


def load():
    if not os.path.exists(DATA_FILE):
        return {"transactions": [], "budget": dict(EMPTY_DATA["budget"])}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"transactions": [], "budget": dict(EMPTY_DATA["budget"])}
    data.setdefault("transactions", [])
    data.setdefault("budget", dict(EMPTY_DATA["budget"]))
    return data


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)