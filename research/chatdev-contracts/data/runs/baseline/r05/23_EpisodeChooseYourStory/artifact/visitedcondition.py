class Condition:
    """Base class for all conditions. Subclasses implement evaluate()."""
    def evaluate(self, state) -> bool:
        raise NotImplementedError("Subclasses must implement evaluate().")
    @staticmethod
    def from_dict(data) -> "Condition":
        """Build a Condition from a dictionary. Dispatches on data['type']."""
        if not isinstance(data, dict) or "type" not in data:
            raise ValueError(f"Invalid condition specification: {data!r}")
        ctype = data["type"]
        if ctype == "has_item":
            return HasItemCondition(data["item"])
        if ctype == "not":
            return NotCondition(Condition.from_dict(data["condition"]))
        if ctype == "and":
            return AndCondition([Condition.from_dict(c) for c in data["conditions"]])
        if ctype == "or":
            return OrCondition([Condition.from_dict(c) for c in data["conditions"]])
        if ctype == "flag":
            return FlagCondition(data["name"], data.get("value", True))
        if ctype == "relationship":
            return RelationshipCondition(data["name"], data["op"], data["value"])
        if ctype == "variable":
            return VariableCondition(data["name"], data["op"], data["value"])
        if ctype == "visited":
            return VisitedCondition(data["node"])
        raise ValueError(f"Unknown condition type: {ctype}")
def _compare(actual, op, expected) -> bool:
    """Shared comparison helper for relationship/variable conditions."""
    if op == "eq":
        return actual == expected
    if op == "ne":
        return actual != expected
    if op == "gt":
        return actual > expected
    if op == "gte":
        return actual >= expected
    if op == "lt":
        return actual < expected
    if op == "lte":
        return actual <= expected
    raise ValueError(f"Unknown comparison operator: {op}")
class HasItemCondition(Condition):
    def __init__(self, item):
        self.item = item
    def evaluate(self, state) -> bool:
        return state.has_item(self.item)
class NotCondition(Condition):
    def __init__(self, condition):
        self.condition = condition
    def evaluate(self, state) -> bool:
        return not self.condition.evaluate(state)
class AndCondition(Condition):
    def __init__(self, conditions):
        self.conditions = conditions
    def evaluate(self, state) -> bool:
        return all(c.evaluate(state) for c in self.conditions)
class OrCondition(Condition):
    def __init__(self, conditions):
        self.conditions = conditions
    def evaluate(self, state) -> bool:
        return any(c.evaluate(state) for c in self.conditions)
class FlagCondition(Condition):
    def __init__(self, name, value=True):
        self.name = name
        self.value = value
    def evaluate(self, state) -> bool:
        return state.get_flag(self.name) == self.value
class RelationshipCondition(Condition):
    def __init__(self, name, op, value):
        self.name = name
        self.op = op
        self.value = value
    def evaluate(self, state) -> bool:
        actual = state.get_relationship(self.name)
        return _compare(actual, self.op, self.value)
class VariableCondition(Condition):
    def __init__(self, name, op, value):
        self.name = name
        self.op = op
        self.value = value
    def evaluate(self, state) -> bool:
        actual = state.get_variable(self.name)
        return _compare(actual, self.op, self.value)
class VisitedCondition(Condition):
    def __init__(self, node):
        self.node = node
    def evaluate(self, state) -> bool:
        return state.has_visited(self.node)