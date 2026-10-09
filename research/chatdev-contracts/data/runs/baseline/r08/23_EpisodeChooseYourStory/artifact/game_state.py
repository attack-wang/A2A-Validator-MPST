'''
game_state.py
Player state management for the interactive storytelling game.
Tracks relationship scores with story characters, inventory items, boolean
story flags, and numeric variables. Supports saving/loading progress as JSON
so a playthrough can be resumed.
'''
import json
import os
SAVE_FILE = "savegame.json"
class GameState:
    """Holds every mutable piece of player progress and persists it as JSON."""
    def __init__(self):
        self.relationships = {}   # name -> int score
        self.items = []           # list of item ids
        self.flags = {}           # name -> bool
        self.variables = {}       # name -> int/str value
        self.current_node = "start"
        self.history = []         # visited node ids
        self.choices_made = []    # list of [node_id, choice_text]
    # --- relationships ---
    def set_relationship(self, name, value):
        """Overwrite a relationship score."""
        self.relationships[name] = int(value)
    def modify_relationship(self, name, delta):
        """Add delta to a relationship score (defaults to 0 if unseen)."""
        self.relationships[name] = self.relationships.get(name, 0) + int(delta)
    def get_relationship(self, name, default=0):
        """Read a relationship score."""
        return self.relationships.get(name, default)
    # --- items ---
    def add_item(self, item):
        """Add an item to the inventory (no duplicates)."""
        if item not in self.items:
            self.items.append(item)
    def remove_item(self, item):
        """Remove an item from the inventory if present."""
        if item in self.items:
            self.items.remove(item)
    def has_item(self, item):
        """True if the item is in the inventory."""
        return item in self.items
    # --- flags ---
    def set_flag(self, name, value=True):
        """Set a boolean story flag."""
        self.flags[name] = bool(value)
    def get_flag(self, name, default=False):
        """Read a boolean story flag."""
        return self.flags.get(name, default)
    # --- variables ---
    def set_variable(self, name, value):
        """Overwrite a variable."""
        self.variables[name] = value
    def adjust_variable(self, name, delta):
        """Add delta to a numeric variable (defaults to 0 if unseen)."""
        self.variables[name] = self.variables.get(name, 0) + delta
    def get_variable(self, name, default=None):
        """Read a variable."""
        return self.variables.get(name, default)
    # --- persistence ---
    def save(self, path=SAVE_FILE):
        """Serialize the full state to JSON."""
        data = {
            "relationships": self.relationships,
            "items": self.items,
            "flags": self.flags,
            "variables": self.variables,
            "current_node": self.current_node,
            "history": self.history,
            "choices_made": self.choices_made,
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except OSError:
            return False
    def load(self, path=SAVE_FILE):
        """Restore state from JSON. Returns True on success."""
        if not os.path.exists(path):
            return False
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return False
        self.relationships = data.get("relationships", {})
        self.items = data.get("items", [])
        self.flags = data.get("flags", {})
        self.variables = data.get("variables", {})
        self.current_node = data.get("current_node", "start")
        self.history = data.get("history", [])
        self.choices_made = data.get("choices_made", [])
        return True
    def clear_save(self, path=SAVE_FILE):
        """Delete the save file (used after an ending is reached)."""
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass
    def summary(self):
        """Human-readable status report for the 's' command."""
        rels = ", ".join(f"{k}: {v:+d}" for k, v in sorted(self.relationships.items())) or "none"
        items = ", ".join(self.items) or "none"
        flags = ", ".join(k for k, v in self.flags.items() if v) or "none"
        variables = ", ".join(f"{k}: {v}" for k, v in sorted(self.variables.items())) or "none"
        lines = [
            "=== STATUS ===",
            f"Relationships: {rels}",
            f"Items:        {items}",
            f"Flags:        {flags}",
            f"Variables:    {variables}",
            f"Current node: {self.current_node}  |  Scenes visited: {len(self.history)}",
        ]
        return "\n".join(lines)