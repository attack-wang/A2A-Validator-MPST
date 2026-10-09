'''
effects.py
State mutations applied when scenes are entered or choices are made.
Mirrors conditions.py: every effect knows how to apply(state) and describe()
itself, and can be built from a structured dictionary spec (see build_effect).
Spec format examples:
    {"type": "add_item", "item": "silver_key"}
    {"type": "adjust_relationship", "who": "rowan", "delta": 2}
    {"type": "set_flag", "flag": "blessed"}
    {"type": "adjust_variable", "name": "composure", "delta": -1}
'''
class Effect:
    """Base class for all state-mutating effects."""
    def apply(self, state):
        raise NotImplementedError("Effect subclasses must implement apply().")
    def describe(self):
        raise NotImplementedError("Effect subclasses must implement describe().")
class AddItem(Effect):
    def __init__(self, item):
        self.item = item
    def apply(self, state):
        if self.item not in state.items:
            state.items.append(self.item)
    def describe(self):
        return f"You obtained: {self.item.replace('_', ' ').title()}."