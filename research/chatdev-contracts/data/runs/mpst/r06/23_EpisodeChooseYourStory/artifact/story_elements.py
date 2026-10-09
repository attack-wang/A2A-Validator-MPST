'''
story_elements.py
Scene and Choice objects...
'''
from conditions import build_condition, build_conditions
from effects import build_effects
class Choice:
    def __init__(self, text, target, effects=None, conditions=None):
        self.text = text
        self.target = target
        self.effects = build_effects(effects)
        self.conditions = build_conditions(conditions)
    def is_available(self, state):
        return all(c.evaluate(state) for c in self.conditions)
    def requirement_text(self):
        return "; ".join(c.describe() for c in self.conditions)
    def describe(self, index, locked=False):
        ...