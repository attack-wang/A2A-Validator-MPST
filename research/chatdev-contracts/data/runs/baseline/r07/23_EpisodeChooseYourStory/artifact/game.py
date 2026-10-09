'''
game.py
Defines the Game class: the interactive console front-end. It renders
narrative segments, presents available (and locked) choices, reads player
input, applies effects, and supports special commands (status, save,
load, help, quit).
'''
import json
import os
import sys
from game_state import GameState
from story_engine import StoryEngine
from story_data import get_story
class Game:
    """Interactive console front-end for the storytelling engine."""
    SAVE_FILE = "savegame.json"
    def __init__(self):
        """Create the game with a story engine and a fresh player state."""
        self.engine = StoryEngine(get_story())
        self.state = GameState()
    def start(self):
        """Run the main game loop until an ending or quit command."""
        print("=" * 60)
        print(self.engine.title.center(60))
        print("=" * 60)
        print(self.engine.intro)
        current = self.engine.get_start_node()
        while True:
            self.state.record_visit(current.id)
            self.display_node(current)
            if current.is_ending:
                self.show_ending_summary()
                return
            available = self.engine.available_choices(current, self.state)
            locked = self.engine.locked_choices(current, self.state)
            self.display_choices(available, locked)
            choice = self.get_choice_input(len(available), current)
            if choice is None:
                continue  # special command handled; re-render node
            self.engine.apply_effects(choice.effects, self.state)
            current = self.engine.get_node(choice.target)
            if current is None:
                print("Story error: missing node.")
                return