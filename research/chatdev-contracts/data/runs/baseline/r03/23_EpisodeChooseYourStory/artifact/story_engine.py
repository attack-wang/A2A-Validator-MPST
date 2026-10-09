'''
story_engine.py
Core branching-narrative engine. Resolves conditional text variants,
filters available choices by game-state conditions, applies choice
effects and detects ending nodes.
'''
class StoryEngine:
    def __init__(self, story_data, game_state):
        self.story = story_data
        self.state = game_state
    def get_node(self, node_id):
        try:
            return self.story[node_id]
        except KeyError:
            raise KeyError(f"Unknown node: {node_id}")
    def resolve_text(self, node):
        for variant in node.get("text_variants", []):
            if self.state.check_conditions(variant.get("conditions", {})):
                return variant.get("text", node.get("text", ""))
        return node.get("text", "")
    def available_choices(self, node):
        return [c for c in node.get("choices", []) if self.state.check_conditions(c.get("conditions", {}))]
    def apply_choice(self, node, choice_index):
        choices = self.available_choices(node)
        if not choices:
            raise ValueError("No choices are available at this node.")
        if not 0 <= choice_index < len(choices):
            raise IndexError(f"Choice index {choice_index} out of range.")
        choice = choices[choice_index]
        self.state.apply_effects(choice.get("effects", {}))
        next_id = choice.get("next")
        if not next_id:
            raise KeyError(
                f"Choice '{choice.get('text', '?')}' has no valid 'next' node."
            )
        return next_id
    def is_ending(self, node):
        return "ending" in node or not node.get("choices")
    def ending_info(self, node):
        info = node.get("ending", {})
        return info.get("type", "neutral"), info.get("title", "The End")
    def start_node_id(self):
        return "start" if "start" in self.story else next(iter(self.story))