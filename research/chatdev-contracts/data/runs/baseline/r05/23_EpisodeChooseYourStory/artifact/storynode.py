'''
storynode.py — StoryNode: one narrative segment with conditional text
variants, player choices, and ending markers. Built from story JSON via
StoryNode.from_dict(data, node_id).
'''
from choice import Choice
from conditions import Condition
from effects import build_effects
class StoryNode:
    ...