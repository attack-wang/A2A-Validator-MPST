'''
conditions.py
Evaluates condition dicts against a GameState. A condition of None
always passes. Compound types ("and"/"or"/"not") nest recursively.
'''
class ConditionError(Exception):
    """Raised when a condition dict is malformed or of an unknown type."""
def evaluate_condition(condition, game_state):
    """Return True when the condition holds for the given game state."""
    if condition is None:
        return True
    ctype = condition.get("type")
    if ctype == "has_item":
        return condition["item"] in game_state.items
    if ctype == "flag_set":
        return condition["flag"] in game_state.flags
    if ctype == "relationship_at_least":
        return game_state.relationships.get(condition["character"], 0) >= condition["value"]
    if ctype == "variable_at_least":
        return game_state.variables.get(condition["name"], 0) >= condition["value"]
    if ctype == "and":
        return all(evaluate_condition(c, game_state) for c in condition["conditions"])
    if ctype == "or":
        return any(evaluate_condition(c, game_state) for c in condition["conditions"])
    if ctype == "not":
        return not evaluate_condition(condition["condition"], game_state)
    raise ConditionError(f"Unknown condition type: {ctype!r}")