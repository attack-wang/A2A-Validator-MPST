from conditions import evaluate
def resolve_next(entry, state):
    if entry is None:
        raise ValueError(...)
    if isinstance(entry, str):
        return entry
    if not isinstance(entry, list) or not entry:
        raise ValueError(...)
    for route in entry:
        cond = route.get("condition")
        if cond is None or evaluate(cond, state):
            return route["next"]
    return entry[-1]["next"]