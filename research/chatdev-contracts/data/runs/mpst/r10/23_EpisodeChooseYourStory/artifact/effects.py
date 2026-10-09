def apply_effects(state, effects):
    if not effects:
        return
    for name, delta in effects.get("variables", {}).items():
        state.change_variable(name, delta)
    for name, value in effects.get("set_variables", {}).items():
        state.set_variable(name, value)
    for item in effects.get("add_items", []):
        state.add_item(item)
    for item in effects.get("remove_items", []):
        state.remove_item(item)
    for flag in effects.get("set_flags", []):
        state.set_flag(flag)
    for flag in effects.get("clear_flags", []):
        state.clear_flag(flag)