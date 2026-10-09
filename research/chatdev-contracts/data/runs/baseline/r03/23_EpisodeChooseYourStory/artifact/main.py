elif isinstance(value, int):
    try:
        node_id = engine.apply_choice(node, value)
    except (ValueError, IndexError, KeyError) as exc:
        ui.message(f"Could not proceed: {exc}")
    continue