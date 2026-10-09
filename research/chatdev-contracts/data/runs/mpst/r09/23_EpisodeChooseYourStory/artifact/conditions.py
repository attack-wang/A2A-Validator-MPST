import json
import os
import conditions
import gamestate
import routing
import ui
STORY_FILE = "story.json"
SAVE_FILE = "save.json"
AUTOSAVE_FILE = "autosave.json"
ENDINGS_FILE = "endings.json"
class GameEngine:
    def __init__(self):
        self.state = gamestate.GameState()
        self.story = self._load_story()
    @staticmethod
    def _load_story():
        try:
            with open(STORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise SystemExit(f"Could not read story data ({STORY_FILE}): {e}")
        scenes = data.get("scenes", {})
        if not scenes:
            raise SystemExit(f"Story file {STORY_FILE} contains no scenes.")
        return scenes
    def _get_scene(self, scene_id):
        try:
            return self.story[scene_id]
        except KeyError:
            raise RuntimeError(f"Scene {scene_id!r} is not defined in the story.")
    def run(self):
        ui.title_banner()
        action = self.main_menu()
        if action == "load":
            try:
                self.state = self.load_game(SAVE_FILE)
            except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
                ui.print_wrapped(f"Could not load save: {e}. Starting a new game.")
                self.state = gamestate.GameState()
        elif action == "quit":
            return
        if not self.intro():
            return
        self.game_loop()
    def main_menu(self):
        while True:
            ui.print_wrapped("1. New game\n2. Load game\n3. Quit")
            choice = ui.pause("Choose an option: ")  # hmm pause uses input(message)
            ...