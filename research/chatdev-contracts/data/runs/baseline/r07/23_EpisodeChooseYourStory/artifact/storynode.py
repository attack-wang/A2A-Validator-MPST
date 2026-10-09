'''
storynode.py
Defines the StoryNode class. Each StoryNode is one narrative segment in
the story graph, holding its text, its branching choices, and (for final
nodes) its ending classification.
'''
from choice import Choice
class StoryNode:
    """Represents a single narrative segment with branching choices."""
    def __init__(self, node_id, text, choices=None, is_ending=False, ending_type=None, ending_name=None):
        """Initialize a StoryNode with an id, narrative text and optional choices."""
        self.id = node_id
        self.text = text
        self.choices = choices or []
        self.is_ending = is_ending
        self.ending_type = ending_type  # "good", "bad", "neutral", "secret"
        self.ending_name = ending_name
    @classmethod
    def from_dict(cls, data):
        """Build a StoryNode from a plain dictionary (story data)."""
        choices = [Choice.from_dict(c) for c in data.get("choices", [])]
        return cls(
            node_id=data["id"],
            text=data["text"],
            choices=choices,
            is_ending=data.get("is_ending", False),
            ending_type=data.get("ending_type"),
            ending_name=data.get("ending_name"),
        )