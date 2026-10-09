class StoryEngine:
    """Indexes story nodes and drives branching advancement."""
    def __init__(self, story_data: dict):
        self.title = story_data.get("title", "Untitled Story")
        self.start_node = story_data.get("start", "start")
        self.nodes = {}
        for node_id, node_data in story_data.get("nodes", {}).items():
            self.nodes[node_id] = StoryNode.from_dict(node_data, node_id)
    def get_node(self, node_id) -> StoryNode:
        if node_id not in self.nodes:
            raise KeyError(f"Unknown story node: {node_id}")
        return self.nodes[node_id]
    def get_available_choices(self, node, state):
        """Return (available, locked) lists of Choice objects."""
        available = [c for c in node.choices if c.is_available(state)]
        locked = [c for c in node.choices if not c.is_available(state)]
        return available, locked
    def apply_effects(self, effects, state):
        for effect in effects:
            effect.apply(state)
    def enter_node(self, state, node_id) -> StoryNode:
        """Mark node visited, apply its on_enter effects, return the node."""
        node = self.get_node(node_id)
        state.current_node = node_id
        state.visit(node_id)
        self.apply_effects(node.on_enter, state)
        return node
    def advance(self, state, node, choice) -> str:
        """Apply the chosen choice's effects, mark it taken, return target id."""
        self.apply_effects(choice.effects, state)
        if choice.once:
            state.mark_choice_taken(choice.node_id, choice.index)
        return choice.target