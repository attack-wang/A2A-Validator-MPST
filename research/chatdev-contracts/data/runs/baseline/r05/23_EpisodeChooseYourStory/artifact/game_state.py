'''
game_state.py — The player's persistent state for a single playthrough.
Tracks relationships (name -> int), inventory (list of item ids), flags
(name -> bool), free-form numeric/string variables, which story nodes have
been visited, and which choices have been taken (for "once" choices).
Supports JSON-safe serialization via to_dict()/from_dict().
'''