'''
story_nodes.py
Data classes for the story graph: Choice (a player option with target node,
gating conditions and consequences) and StoryNode (a narrative segment with
text, optional on-enter effects, conditional text variants, choices, and
ending metadata).
'''
class Choice:
    """A player option with a target node, gating conditions and effects."""
    def __init__(self, text, target, conditions=None, effects=None, locked_hint=None):
        self.text = text                      # label shown to the player
        self.target = target                  # node id this choice leads to
        self.conditions = conditions or []    # list of condition dicts; all must pass
        self.effects = effects or []          # list of effect dicts applied on pick
        self.locked_hint = locked_hint        # custom hint shown when locked
    def is_available(self, state, evaluator):
        """True if every gating condition passes for the current state."""
        for condition in self.conditions:
            if not evaluator.evaluate(condition, state):
                return False
        return True
    def describe_locked(self, state, evaluator):
        """Human-readable reason this choice is currently locked."""
        if self.locked_hint:
            return self.locked_hint
        # Describe the first failing condition for transparency.
        for condition in self.conditions:
            if not evaluator.evaluate(condition, state):
                return evaluator.describe(condition)
        return "locked"
class StoryNode:
    """A narrative segment with text, on-enter effects, variants and choices."""
    def __init__(self, node_id, text, choices=None, on_enter=None,
                 is_ending=False, ending_name=None, ending_tone="neutral",
                 variants=None):
        self.node_id = node_id
        self.text = text
        self.choices = choices or []
        self.on_enter = on_enter or []
        self.is_ending = is_ending
        self.ending_name = ending_name
        self.ending_tone = ending_tone
        # variants: list of {"condition": {...}, "text": "..."} appended to
        # the base text when their condition passes — this is how earlier
        # decisions visibly influence later narrative segments.
        self.variants = variants or []