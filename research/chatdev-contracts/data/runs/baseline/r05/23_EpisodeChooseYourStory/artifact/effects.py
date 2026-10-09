class ConditionalEffect(Effect):
    """Applies its sub-effects only when its condition passes."""
    def __init__(self, requires, effects):
        self.requires = requires
        self.effects = effects
    def apply(self, state):
        if self.requires is None or self.requires.evaluate(state):
            for effect in self.effects:
                effect.apply(state)