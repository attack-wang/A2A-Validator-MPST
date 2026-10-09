'''
choice.py — A player-facing option on a story node.
...
'''
from conditions import Condition
from effects import build_effects
class Choice:
    def __init__(self, text, target, requires=None, effects=None, once=False,
                 node_id=None, index=None):
        self.text = text
        self.target = target
        self.requires = requires
        self.effects = effects or []
        self.once = once
        self.node_id = node_id
        self.index = index
    def key(self):
        return f"{self.node_id}:{self.index}"
    def is_available(self, state) -> bool:
        if self.requires is not None and not self.requires.evaluate(state):
            return False
        if self.once and self.node_id is not None and state.has_choice_been_taken(self.node_id, self.index):
            return False
        return True
    def lock_reason(self, state) -> str:
        """Human-readable hint for why this choice is locked."""
        if self.once and self.node_id is not None and state.has_choice_been_taken(self.node_id, self.index):
            return "already taken"
        if self.requires is not None and not self.requires.evaluate(state):
            return "requirement not met"
        return "unavailable"
    @staticmethod
    def from_dict(data, node_id=None, index=None) -> "Choice":
        requires = Condition.from_dict(data["requires"]) if "requires" in data else None
        effects = build_effects(data.get("effects"))
        return Choice(
            text=data["text"],
            target=data["target"],
            requires=requires,
            effects=effects,
            once=bool(data.get("once", False)),
            node_id=node_id,
            index=index,
        )