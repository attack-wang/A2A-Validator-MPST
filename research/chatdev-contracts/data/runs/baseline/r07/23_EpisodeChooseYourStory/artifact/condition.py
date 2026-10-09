'''
condition.py
Defines the Condition class used for conditional checks that shape the
storyline. A Condition is evaluated against a GameState to decide whether
a choice is available to the player.
'''
class Condition:
    """Represents a conditional check evaluated against the GameState.
    Supported condition types:
      - "variable": compares a state variable to `value` using `operator`
        (one of "eq", "ne", "gt", "gte", "lt", "lte").
      - "item": checks whether the player's inventory contains `name`.
      - "flag": checks whether boolean flag `name` equals `value`.
    """
    def __init__(self, condition_type, name, operator="eq", value=None):
        """Initialize a Condition with a type, target name, operator and value."""
        self.condition_type = condition_type  # "variable", "item", or "flag"
        self.name = name
        self.operator = operator  # comparison operator, used by "variable" type
        self.value = value
    def check(self, state):
        """Return True if this condition is satisfied by the given GameState."""
        if self.condition_type == "variable":
            current = state.get_variable(self.name, default=0)
            if self.operator == "eq":
                return current == self.value
            if self.operator == "ne":
                return current != self.value
            if self.operator == "gt":
                return current > self.value
            if self.operator == "gte":
                return current >= self.value
            if self.operator == "lt":
                return current < self.value
            if self.operator == "lte":
                return current <= self.value
            return False
        if self.condition_type == "item":
            return state.has_item(self.name)
        if self.condition_type == "flag":
            return bool(state.get_flag(self.name, default=False)) == bool(self.value)
        return False
    @classmethod
    def from_dict(cls, data):
        """Build a Condition from a plain dictionary (story data)."""
        return cls(
            condition_type=data["condition_type"],
            name=data["name"],
            operator=data.get("operator", "eq"),
            value=data.get("value"),
        )