class GameState:
    def __init__(self, player_name="Traveler"):
        self.player_name = player_name
        self.flags = {}
        self.items = []
        self.relationships = {}
        self.visited = []
        self.history = []  # list of (scene_id, choice_text)
        self.current_scene = None
        self.turn_count = 0
    def add_item, remove_item, has_item
    def set_flag, get_flag, clear_flag
    def adjust_relationship(name, delta), get_relationship
    def mark_visited(scene_id), has_visited
    def to_dict / from_dict (for save/load)