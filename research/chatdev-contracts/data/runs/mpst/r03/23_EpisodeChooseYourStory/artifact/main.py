"""
DOCSTRING content
"""
import sys
class GameState:
    """Tracks items, numeric variables, and story flags for the player."""
    def __init__(self):
        """Initialize empty inventory, variable table, and flag set."""
        self.items = set()
        self.variables = {}
        self.flags = set()
    def add_item(self, item):
        """Add an item to the player's inventory."""
        self.items.add(item)
    def remove_item(self, item):
        """Remove an item from inventory if present."""
        self.items.discard(item)
    def has_item(self, item):
        """Return True if the item is in the inventory."""
        return item in self.items
    def adjust_var(self, name, delta):
        """Adjust a numeric variable by delta (creates it at 0 if missing)."""
        self.variables[name] = self.variables.get(name, 0) + delta
    def get_var(self, name):
        """Return the current value of a variable (0 if unset)."""
        return self.variables.get(name, 0)
    def set_flag(self, flag):
        """Record a one-time story flag."""
        self.flags.add(flag)
    def has_flag(self, flag):
        """Return True if the flag has been set."""
        return flag in self.flags
    def summary(self):
        """Return a short status string for the HUD line."""
        ...
def evaluate_condition(cond, state):
    """Recursively evaluate a condition dictionary against the game state."""
    ...
def apply_effects(effects, state):
    """Apply a choice's effects dict to the game state."""
    ...
STORY = { ... }
def get_available_choices(node, state):
    """Filter a node's choices, keeping only those whose conditions pass."""
    ...
def prompt_choice(choices):
    """Display numbered choices and validate user input."""
    ...
def main():
    """Run the main game loop."""
    ...
if __name__ == "__main__":
    main()