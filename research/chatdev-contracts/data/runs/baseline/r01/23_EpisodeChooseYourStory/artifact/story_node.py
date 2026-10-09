'''
story_node.py
Defines StoryNode and Choice: the structural building blocks of the branching
narrative graph.
'''
class Choice:
    def __init__(self, text, target, conditions=None, effects=None, locked_text=None):
        ...
    def is_available(self, game_state):
        ...
    def describe(self, game_state):
        ...
class StoryNode:
    def __init__(self, node_id, text, choices=None, effects=None, is_ending=False, ending_label=None):
        ...
    def apply_effects(self, game_state):
        ...
    @classmethod
    def from_dict(cls, node_id, data):
        ...