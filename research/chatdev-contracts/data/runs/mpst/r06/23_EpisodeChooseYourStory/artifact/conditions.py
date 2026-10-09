'''
conditions.py
Conditional checks used to shape the storyline.
Every condition wraps a predicate over the player's GameState and can be
built from a structured dictionary spec (see build_condition). Conditions
are used to gate choices, unlock conditional narrative text, and steer the
story toward different endings.
Spec format examples:
    {"type": "has_item", "item": "silver_key"}
    {"type": "relationship_at_least", "who": "rowan", "value": 2}
    {"type": "flag_set", "flag": "blessed"}
    {"type": "variable_at_least", "name": "composure", "value": 2}
    {"type": "all_of", "conditions": [ ... ]}
'''
def _pretty(name):
    return str(name).replace("_", " ").title()
class Condition:
    """Base class for all conditional checks."""
    def evaluate(self, state):
        """Return True if the condition holds for the given GameState."""
        raise NotImplementedError("Condition subclasses must implement evaluate().")
    def describe(self):
        """Human-readable description, e.g. 'requires the Silver Key'."""
        raise NotImplementedError("Condition subclasses must implement describe().")
class HasItem(Condition):
    def __init__(self, item):
        self.item = item
    def evaluate(self, state):
        return self.item in state.items
    def describe(self):
        return f"requires {_pretty(self.item)}"
...