'''
story_engine.py
Loads structured story data, validates it, drives scene transitions,
applies effects, evaluates conditions, and supports save/load.
'''
import json
from collections import deque
from game_state import GameState
from story_elements import Scene, Choice
from conditions import build_condition, build_conditions
from effects import build_effects
class StoryError(Exception):
    """Raised when story data is malformed."""
class StoryEngine:
    def __init__(self, story_data, state=None):
        self.title = story_data.get("title", "Untitled Story")
        self.intro = story_data.get("intro", "")
        self.start_scene = story_data.get("start")
        self.scenes = {}
        self.state = state or GameState()
        self.pending_messages = []   # feedback from effects, shown by the UI
        self.load_story(story_data)
        self.validate()
        if self.state.current_scene_id is None:
            self.enter_scene(self.start_scene)