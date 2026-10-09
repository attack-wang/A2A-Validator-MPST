'''
effects.py — Effect classes for mutating the GameState when choices are made
or story nodes are entered.
Each Effect subclass implements apply(state). Effects are constructed from
dictionaries via Effect.from_dict(data), which dispatches on the "type" key.
Supported types:
    add_item, remove_item, set_flag, clear_flag, set_relationship,
    add_relationship, set_variable, add_variable
'''