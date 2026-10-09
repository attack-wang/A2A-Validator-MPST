class GameEngine:
    def __init__(self, story, ui, state=None):
        ...
    def start_new_game(self)
    def run(self)  # main loop
    def _play_node(self, node_id)  # returns next node id or None for ending/quit
    def _available_choices(self, node)
    def _apply_effects(self, effects)
    def _resolve_auto(self, node)