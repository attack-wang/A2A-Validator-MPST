import json
import os

DATA_FILE = "budget_data.json"


def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and isinstance(data.get("transactions"), list):
                data.setdefault("savings_goal", 0.0)
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {"transactions": [], "savings_goal": 0.0}


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)