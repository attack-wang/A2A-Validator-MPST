def check_conditions(state, conditions):
    if not conditions:
        return True
    for name, minimum in conditions.get("min_variables", {}).items():
        if state.get_variable(name) < minimum:
            return False
    for name, maximum in conditions.get("max_variables", {}).items():
        if state.get_variable(name) > maximum:
            return False
    for item in conditions.get("has_items", []):
        if not state.has_item(item):
            return False
    for item in conditions.get("not_has_items", []):
        if state.has_item(item):
            return False
    for flag in conditions.get("flags", []):
        if not state.has_flag(flag):
            return False
    for flag in conditions.get("not_flags", []):
        if state.has_flag(flag):
            return False
    for node_id in conditions.get("visited", []):
        if node_id not in [h[0] for h in state.history]:
            return False
    for node_id in conditions.get("not_visited", []):
        if node_id in [h[0] for h in state.history]:
            return False
    return True