'''
game_state.py
Tracks the player's mutable state: inventory items, story flags,
character relationships, numeric variables and visit history.
Provides effect application, condition checking and JSON persistence.
'''
import json
import copy
import os
RELATIONSHIP_MIN = -10
RELATIONSHIP_MAX = 10
class GameState:
    def __init__(self):
        self.items = []
        self.flags = {}
        self.relationships = {}
        self.variables = {}
        self.history = []
    # ----- inventory -----
    def add_item(self, item):
        if item and item not in self.items:
            self.items.append(item)
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    def has_item(self, item):
        return item in self.items
    def has_items(self, items):
        return all(self.has_item(i) for i in items)
    # ----- flags -----
    def set_flag(self, name, value=True):
        self.flags[name] = value
    def get_flag(self, name, default=None):
        return self.flags.get(name, default)
    # ----- relationships -----
    def adjust_relationship(self, who, delta):
        current = self.relationships.get(who, 0)
        self.relationships[who] = max(RELATIONSHIP_MIN, min(RELATIONSHIP_MAX, current + delta))
    def get_relationship(self, who):
        return self.relationships.get(who, 0)
    # ----- variables -----
    def adjust_variable(self, name, delta):
        self.variables[name] = self.variables.get(name, 0) + delta
    def set_variable(self, name, value):
        self.variables[name] = value
    def get_variable(self, name, default=0):
        return self.variables.get(name, default)
    # ----- effects & conditions -----
    def apply_effects(self, effects):
        if not effects:
            return
        for item in effects.get("add_items", []):
            self.add_item(item)
        for item in effects.get("remove_items", []):
            self.remove_item(item)
        for name, value in effects.get("set_flags", {}).items():
            self.set_flag(name, value)
        for who, delta in effects.get("adjust_relationships", {}).items():
            self.adjust_relationship(who, delta)
        for name, delta in effects.get("adjust_variables", {}).items():
            self.adjust_variable(name, delta)
        for name, value in effects.get("set_variables", {}).items():
            self.set_variable(name, value)
    def check_conditions(self, conditions):
        if not conditions:
            return True
        for item in conditions.get("items", []):
            if not self.has_item(item):
                return False
        for item in conditions.get("not_items", []):
            if self.has_item(item):
                return False
        for name, value in conditions.get("flags", {}).items():
            if self.flags.get(name) != value:
                return False
        for who, value in conditions.get("relationships", {}).items():
            if self.get_relationship(who) < value:
                return False
        for name, value in conditions.get("variables", {}).items():
            if self.get_variable(name) < value:
                return False
        return True
    # ----- persistence -----
    def to_dict(self):
        return {
            "items": list(self.items),
            "flags": dict(self.flags),
            "relationships": dict(self.relationships),
            "variables": dict(self.variables),
            "history": list(self.history),
        }
    def from_dict(self, data):
        if not isinstance(data, dict):
            raise ValueError("Save data must be a JSON object.")
        self.items = [str(i) for i in data.get("items", []) if isinstance(i, str)]
        flags = data.get("flags", {})
        self.flags = {str(k): v for k, v in flags.items()} if isinstance(flags, dict) else {}
        relationships = data.get("relationships", {})
        self.relationships = (
            {str(k): int(v) for k, v in relationships.items()}
            if isinstance(relationships, dict) else {}
        )
        variables = data.get("variables", {})
        self.variables = (
            {str(k): v for k, v in variables.items()}
            if isinstance(variables, dict) else {}
        )
        history = data.get("history", [])
        self.history = [str(h) for h in history if isinstance(h, str)]
        return self
    def save_to_file(self, path, current_node):
        payload = {"current_node": current_node, "state": self.to_dict()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    def load_from_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        self.from_dict(payload.get("state", {}))
        return payload.get("current_node", "start")