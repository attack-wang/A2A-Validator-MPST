'''
game_state.py
Defines the GameState class, which tracks every dynamic piece of player
progress in the interactive story: arbitrary variables, inventory items,
relationship scores with characters, one-shot event flags, the history of
visited story nodes, choices made, and endings discovered. Supports
serialization to/from plain dictionaries so the SaveManager can persist
and restore a run.
'''
import json
class GameState:
    """Tracks variables, inventory, relationships, flags and node history."""
    def __init__(self):
        self.variables = {}        # name -> value (int/str/bool)
        self.inventory = []        # list of item ids
        self.relationships = {}    # character -> int affinity
        self.flags = set()         # names of one-shot events that occurred
        self.history = []          # ordered list of visited node ids
        self.choices_made = []     # ordered list of (node_id, choice_text)
        self.endings_discovered = []  # ordered list of ending node ids
    # ----- inventory -----
    def add_item(self, item):
        """Add an item to inventory if not already present."""
        if item not in self.inventory:
            self.inventory.append(item)
    def remove_item(self, item):
        """Remove an item from inventory if present."""
        if item in self.inventory:
            self.inventory.remove(item)
    def has_item(self, item):
        """Return True if the item is currently held."""
        return item in self.inventory
    # ----- relationships -----
    def ensure_relationship(self, character, default=0):
        """Guarantee a relationship entry exists, returning its value."""
        if character not in self.relationships:
            self.relationships[character] = default
        return self.relationships[character]
    def adjust_relationship(self, character, delta):
        """Adjust a relationship score, creating it at 0 if unknown."""
        self.ensure_relationship(character)
        self.relationships[character] += delta
    def get_relationship(self, character):
        """Return the relationship score (0 if the character is unknown)."""
        return self.relationships.get(character, 0)
    # ----- flags -----
    def set_flag(self, flag):
        """Mark a one-shot event as having occurred."""
        self.flags.add(flag)
    def clear_flag(self, flag):
        """Remove a flag if present."""
        self.flags.discard(flag)
    def has_flag(self, flag):
        """Return True if the flag has been set."""
        return flag in self.flags
    # ----- variables -----
    def set_variable(self, name, value):
        """Set a named variable to a value."""
        self.variables[name] = value
    def get_variable(self, name, default=None):
        """Return a variable's value or a default if unset."""
        return self.variables.get(name, default)
    # ----- history -----
    def record_visit(self, node_id):
        """Append a node id to the visit history."""
        self.history.append(node_id)
    def record_choice(self, node_id, choice_text):
        """Append a (node_id, choice_text) tuple to the choice log."""
        self.choices_made.append((node_id, choice_text))
    def record_ending(self, node_id):
        """Append an ending node id to the endings-discovered log."""
        self.endings_discovered.append(node_id)
    # ----- serialization -----
    def to_dict(self):
        """Serialize state to a JSON-safe dict (set -> sorted list)."""
        return {
            "variables": dict(self.variables),
            "inventory": list(self.inventory),
            "relationships": dict(self.relationships),
            "flags": sorted(self.flags),  # set is not JSON-serializable
            "history": list(self.history),
            "choices_made": [list(pair) for pair in self.choices_made],
            "endings_discovered": list(self.endings_discovered),
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a GameState from a serialized dict (list -> set)."""
        state = cls()
        state.variables = dict(data.get("variables", {}))
        state.inventory = list(data.get("inventory", []))
        state.relationships = dict(data.get("relationships", {}))
        state.flags = set(data.get("flags", []))
        state.history = list(data.get("history", []))
        state.choices_made = [tuple(pair) for pair in data.get("choices_made", [])]
        state.endings_discovered = list(data.get("endings_discovered", []))
        return state
    def save_to_file(self, path):
        """Write serialized state to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
    @classmethod
    def load_from_file(cls, path):
        """Read a JSON file and rebuild a GameState."""
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))