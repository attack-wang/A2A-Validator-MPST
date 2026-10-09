def apply(effects, state):
    changes = []
    keys: "add_items" (list), "remove_items" (list), "set_flags" (dict name->value), "clear_flags" (list), "adjust_relationships" (dict name->int), "set_relationships" (dict name->int)
    returns list of human-readable strings like "Acquired: Moonpetal", "Maren +2 (now 4)"