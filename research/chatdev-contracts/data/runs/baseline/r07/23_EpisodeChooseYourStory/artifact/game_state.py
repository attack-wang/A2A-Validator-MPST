'''
game_state.py
Defines the GameState class, which tracks all player progress: numeric
variables (e.g., relationship levels), inventory items, boolean flags,
the current node, and visit history. Supports serialization for save/load.
'''
class GameState:
    """Tracks all player state: variables, items, flags, position and history."""
    def __init__(self):
        """Initialize a fresh GameState with empty containers."""
        self.variables = {}
        self.items = []
        self.flags = {}
        self.current_node_id = None
        self.history = []
        self.visited_nodes = []
    def set_variable(self, name, value):
        """Set a numeric (or any) variable to the given value."""
        self.variables[name] = value
    def get_variable(self, name, default=0):
        """Return the value of a variable, or `default` if it is unset."""
        return self.variables.get(name, default)
    def add_item(self, name):
        """Add an item to the inventory if it is not already present."""
        if name not in self.items:
            self.items.append(name)
    def remove_item(self, name):
        """Remove an item from the inventory if present."""
        if name in self.items:
            self.items.remove(name)
    def has_item(self, name):
        """Return True if the inventory contains the given item."""
        return name in self.items
    def set_flag(self, name, value=True):
        """Set a boolean flag to the given value."""
        self.flags[name] = value
    def get_flag(self, name, default=False):
        """Return the value of a flag, or `default` if it is unset."""
        return self.flags.get(name, default)
    def record_visit(self, node_id):
        """Record that the player has entered the given node."""
        self.current_node_id = node_id
        self.visited_nodes.append(node_id)
        self.history.append(node_id)
    def to_dict(self):
        """Serialize the state to a plain dictionary for saving."""
        return {
            "variables": dict(self.variables),
            "items": list(self.items),
            "flags": dict(self.flags),
            "current_node_id": self.current_node_id,
            "history": list(self.history),
            "visited_nodes": list(self.visited_nodes),
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a GameState from a dictionary produced by to_dict()."""
        state = cls()
        state.variables = dict(data.get("variables", {}))
        state.items = list(data.get("items", []))
        state.flags = dict(data.get("flags", {}))
        state.current_node_id = data.get("current_node_id")
        state.history = list(data.get("history", []))
        state.visited_nodes = list(data.get("visited_nodes", []))
        return state