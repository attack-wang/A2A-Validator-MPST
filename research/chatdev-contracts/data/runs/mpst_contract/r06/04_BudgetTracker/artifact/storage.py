import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget_data.json")


def load_data():
    default = {"next_id": 1, "transactions": []}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "transactions" in data and "next_id" in data:
                if isinstance(data["transactions"], list) and isinstance(data["next_id"], int):
                    return data
        except (json.JSONDecodeError, OSError, ValueError):
            pass
    return default


def save_data(data):
    tmp = DATA_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, DATA_FILE)
    except OSError:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)