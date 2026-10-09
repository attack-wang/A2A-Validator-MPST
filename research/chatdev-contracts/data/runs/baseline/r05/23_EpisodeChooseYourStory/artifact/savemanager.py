import os
import json
import time
from game_state import GameState
class SaveManager:
    """Handles writing/reading GameState JSON files."""
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
    def _path_for(self, slot) -> str:
        return os.path.join(self.save_dir, f"save_{slot}.json")
    def save(self, state, slot=1) -> str:
        """Write state to the given slot; returns the path written."""
        path = self._path_for(slot)
        payload = {
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "state": state.to_dict(),
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        return path
    def load(self, slot=1) -> GameState:
        """Read a GameState from the given slot; raises FileNotFoundError if absent."""
        path = self._path_for(slot)
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        return GameState.from_dict(payload.get("state", payload))
    def has_save(self, slot=1) -> bool:
        return os.path.exists(self._path_for(slot))