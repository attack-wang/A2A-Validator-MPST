'''
story_engine.py
Defines the StoryEngine class, which loads and validates the structured
story data (a graph of StoryNodes), resolves the current node, filters
choices by conditions, and applies choice effects to the GameState.
'''
from storynode import StoryNode
class StoryEngine:
    """Loads, validates and navigates the structured story graph."""
    def __init__(self, story_data):
        """Parse raw story data into StoryNode objects and validate links."""
        self.nodes = {}
        self.title = story_data.get("title", "Untitled")
        self.intro = story_data.get("intro", "")
        for node_data in story_data["nodes"]:
            node = StoryNode.from_dict(node_data)
            self.nodes[node.id] = node
        self.start_node_id = story_data["start"]
        self.validate()
    def get_node(self, node_id):
        """Return the StoryNode with the given id, or None if it does not exist."""
        return self.nodes.get(node_id)
    def get_start_node(self):
        """Return the starting StoryNode of the story."""
        return self.nodes[self.start_node_id]
    def available_choices(self, node, state):
        """Return the choices of `node` whose conditions pass for `state`."""
        return [c for c in node.choices if c.is_available(state)]
    def locked_choices(self, node, state):
        """Return the choices of `node` whose conditions fail for `state`."""
        return [c for c in node.choices if not c.is_available(state)]
    def apply_effects(self, effects, state):
        """Apply a list of Effect objects to the given GameState."""
        for effect in effects:
            effect.apply(state)
    def validate(self):
        """Check that every choice target points to an existing node.
        Raises ValueError if a dangling target is found.
        """
        for node in self.nodes.values():
            for choice in node.choices:
                if choice.target not in self.nodes:
                    raise ValueError(
                        "Node '{}' has choice targeting missing node '{}'".format(node.id, choice.target)
                    )
        if self.start_node_id not in self.nodes:
            raise ValueError("Start node '{}' does not exist".format(self.start_node_id))