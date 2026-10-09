'''
game_state.py
Defines the player's runtime state (GameState) along with the Condition and
Effect primitives used to gate and mutate that state throughout the story.
'''
class Condition:
    """Represents a conditional check against the GameState."""
    VALID_TYPES = {...}
    def __init__(self, condition_type, **params):
        self.condition_type = condition_type
        self.params = params
    def check(self, game_state):
        ...
    @staticmethod
    def from_dict(data):
        ...
class Effect:
    """Represents a mutation applied to the GameState."""
    def __init__(self, effect_type, **params):
        ...
    def apply(self, game_state):
        ...
    @staticmethod
    def from_dict(data):
        ...
class GameState:
    """Tracks variables, inventory, and visited nodes for one playthrough."""
    def __init__(self):
        self.variables = {}
        self.inventory = set()
        self.visited_nodes = []
        self.current_node_id = None
    def get_variable(self, name, default=0):
        ...
    def set_variable(self, name, value):
        ...
    def modify_variable(self, name, delta):
        ...
    def add_item(self, item):
        ...
    def remove_item(self, item):
        ...
    def has_item(self, item):
        ...
    def mark_visited(self, node_id):
        ...
    def has_visited(self, node_id):
        ...
    def to_dict(self):
        ...
    @classmethod
    def from_dict(cls, data):
        ...