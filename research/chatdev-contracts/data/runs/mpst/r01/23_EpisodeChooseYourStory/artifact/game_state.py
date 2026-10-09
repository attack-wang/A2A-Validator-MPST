'''
game_state.py
Tracks the player's persistent state: items, flags, relationships,
variables, choice history, and visited nodes. Also supports saving
and loading progress to FILENAME as JSON.
'''
import json
FILENAME = "savegame.json"
class GameState:
    """Container for everything that shapes branching and endings."""
    def __init__(self, player_name="Traveler"):
        self.player_name = player_name
        self.items = set()            # item names the player carries
        self.flags = set()            # story flags that have been set
        self.relationships = {}       # character -> level (int)
        self.variables = {}           # variable name -> value (int)
        self.choice_history = []      # list of (node_id, choice_text)
        self.visited_nodes = set()    # node ids entered at least once
    # -- recording ------------------------------------------------------
    def record_choice(self, node_id, choice_text):
        """Append (node_id, choice_text) to the journey history."""
        self.choice_history.append((node_id, choice_text))
    def record_visit(self, node_id):
        """Mark a node as visited (used for one-time on_enter effects)."""
        self.visited_nodes.add(node_id)
    # -- effects ----------------------------------------------------------
    def apply_effects(self, effects):
        """Apply a list of effect dicts (None/empty is a no-op)."""
        if not effects:
            return
        for effect in effects:
            self._apply_one(effect)
    def _apply_one(self, effect):
        etype = effect.get("type")
        if etype == "add_item":
            self.items.add(effect["item"])
        elif etype == "remove_item":
            self.items.discard(effect["item"])
        elif etype == "set_flag":
            self.flags.add(effect["flag"])
        elif etype == "change_relationship":
            who = effect["character"]
            self.relationships[who] = self.relationships.get(who, 0) + effect["delta"]
        elif etype == "increment_variable":
            name = effect["name"]
            self.variables[name] = self.variables.get(name, 0) + effect.get("amount", 1)
        else:
            raise ValueError(f"Unknown effect type: {etype!r}")
    # -- persistence ------------------------------------------------------
    def save(self, filename=FILENAME):
        data = {
            "player_name": self.player_name,
            "items": sorted(self.items),
            "flags": sorted(self.flags),
            "relationships": self.relationships,
            "variables": self.variables,
            "choice_history": self.choice_history,
            "visited_nodes": sorted(self.visited_nodes),
        }
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    @classmethod
    def load(cls, filename=FILENAME):
        with open(filename, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        state = cls(player_name=data.get("player_name", "Traveler"))
        state.items = set(data.get("items", []))
        state.flags = set(data.get("flags", []))
        state.relationships = data.get("relationships", {})
        state.variables = data.get("variables", {})
        state.choice_history = [tuple(p) for p in data.get("choice_history", [])]
        state.visited_nodes = set(data.get("visited_nodes", []))
        return state