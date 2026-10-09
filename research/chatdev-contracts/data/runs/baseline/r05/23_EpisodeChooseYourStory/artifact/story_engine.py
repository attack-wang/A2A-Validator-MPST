'''
story_engine.py — Core story data structures and branching logic.
StoryNode holds narrative text (optionally with conditional variants),
player choices, and ending markers. Choice availability is gated by
Condition objects; taking a choice applies its Effects and moves the
player to the target node. StoryEngine indexes nodes by id and drives
advancement, including per-node "on_enter" effects.
'''