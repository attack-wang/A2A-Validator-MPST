class StoryEngine:
    FALLBACK_ENDING = "ending_lost"  # or from story dict "fallback"
    def __init__(self, story, state, ui): ...
    def run(self): loop as described; dead-end -> fallback ending node
    def available_choices(self, node): returns list of (status, choice)
    def check_conditions(self, conds): delegate to story_data.check_conditions
    def apply_effects(self, effects): dispatch