'''
save_manager.py
Handles persisting and restoring a playthrough (game state + current node)
as JSON so players can resume later.
'''
class SaveManager:
    SAVE_DIRECTORY = "saves"
    @staticmethod
    def save_game(game_state, slot_name):
        ...
    @staticmethod
    def load_game(slot_name):
        ...
    @staticmethod
    def list_saves():
        ...