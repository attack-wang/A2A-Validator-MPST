class SaveManager:
    def __init__(self, directory="saves")
    ensure dir
    def save(state, slot:int) -> str path; filename save_{slot}.json with meta (timestamp, scene title, player name)
    def load(slot) -> GameState or None
    def list_saves() -> list of dicts (slot, name, scene, timestamp)
    def delete(slot)
    endings meta: file "endings.json": def record_ending(name), endings_seen() -> list