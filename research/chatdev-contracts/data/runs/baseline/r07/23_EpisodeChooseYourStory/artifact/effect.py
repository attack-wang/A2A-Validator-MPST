'''
effect.py
Defines the Effect class, representing a state change (variable update,
item gain/loss, or flag toggle) applied when the player makes a choice.
'''
class Effect:
    """Represents a state change applied when a choice is made."""
    def __init__(self, effect_type, name, operator="set", value=None):
        """Initialize an Effect with a type, target name, operator and value."""
        self.effect_type = effect_type  # "variable", "item", "flag"
        self.name = name
        self.operator = operator  # "set"/"add" for variables, "add"/"remove" for items, "set"/"clear" for flags
        self.value = value
    def apply(self, state):
        """Apply this effect to the given GameState."""
        if self.effect_type == "variable":
            if self.operator == "set":
                state.set_variable(self.name, self.value)
            elif self.operator == "add":
                current = state.get_variable(self.name, default=0)
                state.set_variable(self.name, current + self.value)
        elif self.effect_type == "item":
            if self.operator == "add":
                state.add_item(self.name)
            elif self.operator == "remove":
                state.remove_item(self.name)
        elif self.effect_type == "flag":
            if self.operator == "set":
                state.set_flag(self.name, True)
            elif self.operator == "clear":
                state.set_flag(self.name, False)