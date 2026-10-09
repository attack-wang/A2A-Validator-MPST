'''
conditions.py
ConditionEvaluator: interprets declarative condition dictionaries against a
GameState. Conditions gate which choices are visible/available and can also
be attached to nodes. Supported primitives: has_item, flag_set,
relationship_at_least, relationship_at_most, variable_equals,
variable_at_least, variable_at_most, visited, plus combinators and/or/not.
'''
class ConditionError(Exception):
    """Raised when a condition dictionary has an unknown or invalid type."""
class ConditionEvaluator:
    """Evaluates declarative condition dicts against a GameState."""
    def __init__(self):
        # Dispatch table mapping condition type -> handler method.
        self._handlers = {
            "has_item": self._has_item,
            "flag_set": self._flag_set,
            "relationship_at_least": self._relationship_at_least,
            "relationship_at_most": self._relationship_at_most,
            "variable_equals": self._variable_equals,
            "variable_at_least": self._variable_at_least,
            "variable_at_most": self._variable_at_most,
            "visited": self._visited,
            "and": self._and,
            "or": self._or,
            "not": self._not,
        }
    def evaluate(self, condition, state):
        """Evaluate a condition dict; returns True/False.
        Raises ConditionError for unknown types or malformed dicts so that
        typos in story data fail fast instead of silently gating choices.
        """
        if not isinstance(condition, dict) or "type" not in condition:
            raise ConditionError(f"Malformed condition (missing 'type'): {condition!r}")
        ctype = condition["type"]
        handler = self._handlers.get(ctype)
        if handler is None:
            raise ConditionError(f"Unknown condition type: {ctype!r}")
        return handler(condition, state)
    # ----- primitive handlers -----
    def _has_item(self, cond, state):
        """True if the player holds the specified item."""
        return state.has_item(cond["item"])
    def _flag_set(self, cond, state):
        """True if the specified flag has been set."""
        return state.has_flag(cond["flag"])
    def _relationship_at_least(self, cond, state):
        """True if relationship score >= threshold."""
        return state.get_relationship(cond["character"]) >= cond["value"]
    def _relationship_at_most(self, cond, state):
        """True if relationship score <= threshold."""
        return state.get_relationship(cond["character"]) <= cond["value"]
    def _variable_equals(self, cond, state):
        """True if the variable equals the given value."""
        return state.get_variable(cond["name"]) == cond["value"]
    def _variable_at_least(self, cond, state):
        """True if the numeric variable >= threshold."""
        value = state.get_variable(cond["name"], 0)
        return value >= cond["value"]
    def _variable_at_most(self, cond, state):
        """True if the numeric variable <= threshold."""
        value = state.get_variable(cond["name"], 0)
        return value <= cond["value"]
    def _visited(self, cond, state):
        """True if the node id appears in the visit history."""
        return cond["node"] in state.history
    # ----- combinator handlers -----
    def _and(self, cond, state):
        """True only if every sub-condition passes."""
        return all(self.evaluate(sub, state) for sub in cond["conditions"])
    def _or(self, cond, state):
        """True if at least one sub-condition passes."""
        return any(self.evaluate(sub, state) for sub in cond["conditions"])
    def _not(self, cond, state):
        """True if the single sub-condition fails."""
        return not self.evaluate(cond["condition"], state)
    def describe(self, condition):
        """Return a human-readable hint string for locked choices."""
        ctype = condition.get("type", "?") if isinstance(condition, dict) else "?"
        descriptions = {
            "has_item": lambda c: f"requires item: {c.get('item', '?')}",
            "flag_set": lambda c: f"requires event: {c.get('flag', '?')}",
            "relationship_at_least": lambda c: f"requires {c.get('character', '?')} trust >= {c.get('value', '?')}",
            "relationship_at_most": lambda c: f"requires {c.get('character', '?')} trust <= {c.get('value', '?')}",
            "variable_equals": lambda c: f"requires {c.get('name', '?')} == {c.get('value', '?')}",
            "variable_at_least": lambda c: f"requires {c.get('name', '?')} >= {c.get('value', '?')}",
            "variable_at_most": lambda c: f"requires {c.get('name', '?')} <= {c.get('value', '?')}",
            "visited": lambda c: f"requires having visited: {c.get('node', '?')}",
        }
        if ctype in ("and", "or"):
            joiner = " AND " if ctype == "and" else " OR "
            subs = [self.describe(sub) for sub in condition.get("conditions", [])]
            return "(" + joiner.join(subs) + ")"
        if ctype == "not":
            return f"NOT {self.describe(condition.get('condition', {}))}"
        builder = descriptions.get(ctype)
        return builder(condition) if builder else f"requires: {ctype}"