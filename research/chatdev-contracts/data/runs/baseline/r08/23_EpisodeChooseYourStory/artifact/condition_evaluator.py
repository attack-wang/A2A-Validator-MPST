'''
condition_evaluator.py
Conditional logic for shaping the storyline.
Evaluates structured condition dictionaries against the current GameState.
Supported condition types: item possession, relationship thresholds,
boolean flags, and numeric/string variable comparisons. Conditions can be
combined with 'all' / 'any' groups for complex branching rules.
'''
class ConditionEvaluator:
    """Turns declarative condition dicts into booleans against a GameState."""
    @staticmethod
    def evaluate(conditions, state):
        """Evaluate a list of conditions (implicit AND). Empty -> True."""
        if not conditions:
            return True
        return all(ConditionEvaluator._evaluate_single(c, state) for c in conditions)
    @staticmethod
    def _evaluate_single(cond, state):
        """Dispatch a single condition dict to its type-specific check."""
        ctype = cond.get("type")
        op = cond.get("op", "==")
        if ctype == "item":
            has = state.has_item(cond["item"])
            return has if op in ("has", "==", "is") else not has
        if ctype == "relationship":
            value = state.get_relationship(cond["name"], 0)
            return ConditionEvaluator._compare(value, op, cond["value"])
        if ctype == "flag":
            value = state.get_flag(cond["name"], False)
            return value if op in ("is", "==", "true") else not value
        if ctype == "variable":
            value = state.get_variable(cond["name"], 0)
            return ConditionEvaluator._compare(value, op, cond["value"])
        if ctype == "all":
            return all(ConditionEvaluator._evaluate_single(c, state)
                       for c in cond.get("conditions", []))
        if ctype == "any":
            return any(ConditionEvaluator._evaluate_single(c, state)
                       for c in cond.get("conditions", []))
        # Unknown condition types fail safe (branch not taken).
        return False
    @staticmethod
    def _compare(left, op, right):
        """Apply a comparison operator to two values."""
        ops = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            ">=": lambda a, b: a >= b,
            "<": lambda a, b: a < b,
            "<=": lambda a, b: a <= b,
        }
        if op not in ops:
            raise ValueError(f"Unsupported comparison operator: {op!r}")
        return ops[op](left, right)