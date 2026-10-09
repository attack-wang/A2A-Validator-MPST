'''
game_state.py
...
'''
class GameState:
    def __init__(self, starting_scene_id=None):
        self.items = []
        self.relationships = {}
        self.flags = set()
        self.variables = {}
        self.visited = []          # ordered list of visited scene ids (with repeats)
        self.current_scene_id = starting_scene_id
    def to_dict(self): ...
    @classmethod
    def from_dict(cls, data): ...