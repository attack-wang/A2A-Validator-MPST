'''
Player state for the storytelling game.
Tracks inventory items, relationship scores, story flags, the history
of visited scenes, and the current scene id. Provides effect
application and (de)serialization so games can be saved and loaded.
'''
import copy
class GameState:
    """Holds all mutable player/story state and applies scene effects."""
    def __init__(self):
        self.items = []
        self.relationships = {}
        self.flags = {}
        self.history = []
        self.current_scene = "start"
    # ----- inventory -----
    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    def has_item(self, item):
        return item in self.items
    # ----- relationships -----
    def adjust_relationship(self, who, delta):
        self.relationships[who] = self.get_relationship(who) + delta
    def get_relationship(self, who):
        return self.relationships.get(who, 0)
    # ----- flags -----
    def set_flag(self, key, value):
        self.flags[key] = value
    def get_flag(self, key):
        return self.flags.get(key)
    # ----- effects -----
    def apply_effects(self, effects):
        """Apply an effects dict, e.g.:
        {
            "add_items": ["old_map"],
            "remove_items": ["lantern"],
            "relationship": {"mira": 1},
            "flags": {"helped_wolf": True}
        }
        """
        if not effects:
            return
        for item in effects.get("add_items", []):
            self.add_item(item)
        for item in effects.get("remove_items", []):
            self.remove_item(item)
        for who, delta in effects.get("relationship", {}).items():
            self.adjust_relationship(who, delta)
        for key, value in effects.get("flags", {}).items():
            self.set_flag(key, value)
    # ----- serialization -----
    def to_dict(self):
        return {
            "items": list(self.items),
            "relationships": dict(self.relationships),
            "flags": dict(self.flags),
            "history": list(self.history),
            "current_scene": self.current_scene,
        }
    @classmethod
    def from_dict(cls, data):
        state = cls()
        state.items = list(data.get("items", []))
        state.relationships = dict(data.get("relationships", {}))
        state.flags = dict(data.get("flags", {}))
        state.history = list(data.get("history", []))
        state.current_scene = data.get("current_scene", "start")
        return state