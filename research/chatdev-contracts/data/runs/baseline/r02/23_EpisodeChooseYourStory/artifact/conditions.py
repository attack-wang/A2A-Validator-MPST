def evaluate(cond, state):
    if cond is None or cond == {}: return True
    if isinstance(cond, list): return all(evaluate(c, state) for c in cond)
    if isinstance(cond, str): treat as flag name? I'll support string shorthand for flag check.
    must be dict with single key:
    keys: "flag", "not_flag", "has_item", "not_has_item", "relationship_at_least", "relationship_at_most", "visited", "not_visited", "all", "any", "not", "true", "false"