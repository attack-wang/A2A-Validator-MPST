import json, os, re
class SaveManager:
    SAVE_DIRECTORY = "saves"
    @staticmethod
    def _slot_to_path(slot_name):
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", slot_name.strip()) or "quicksave"
        return os.path.join(SaveManager.SAVE_DIRECTORY, safe + ".json")
    @staticmethod
    def save_game(game_state, slot_name):
        os.makedirs(SaveManager.SAVE_DIRECTORY, exist_ok=True)
        payload = {"game_state": game_state.to_dict(), "current_node_id": game_state.current_node_id}
        with open(path, "w", encoding="utf-8") as f: json.dump(payload, f, indent=2)
        return path
    @staticmethod
    def load_game(slot_name):
        path = ...
        if not os.path.exists(path): raise FileNotFoundError(f"No save slot named '{slot_name}'.")
        try: 
            with open... json.load
        except json.JSONDecodeError as e: raise ValueError(f"Save file ... is corrupt") 
        validate keys: "game_state" present
        return data
    @staticmethod
    def list_saves():
        if not os.path.isdir(...): return []
        return sorted(f[:-5] for f in os.listdir(dir) if f.endswith(".json"))