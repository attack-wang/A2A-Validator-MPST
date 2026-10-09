'''
choice.py
Defines the Choice class. Each Choice represents an option presented to
the player, with optional conditions (availability checks) and effects
(state changes applied when chosen).
'''
from condition import Condition
from effect import Effect
class Choice:
    """Represents a branching option offered to the player at a story node."""
    def __init__(self, text, target, conditions=None, effects=None, requirement_text=None):
        """Initialize a Choice with display text, target node, conditions and effects."""
        self.text = text
        self.target = target
        self.conditions = conditions or []
        self.effects = effects or []
        self.requirement_text = requirement_text
    def is_available(self, state):
        """Return True if all conditions are satisfied by the given GameState."""
        return all(c.check(state) for c in self.conditions)
    @classmethod
    def from_dict(cls, data):
        """Build a Choice from a plain dictionary (story data)."""
        conditions = [Condition(**c) if isinstance(c, dict) else c for c in data.get("conditions", [])]
        effects = [Effect(**e) if isinstance(e, dict) else e for e in data.get("effects", [])]
        return cls(
            text=data["text"],
            target=data["target"],
            conditions=conditions,
            effects=effects,
            requirement_text=data.get("requirement_text"),
        )