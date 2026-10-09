'''
game_engine.py
Core rules of the game: player movement on the 80 x 80 grid, combat
resolution, treasure chests, level progression through the door and
the message log shown in the UI.
'''
import random
import game_constants as C
from entities import Player
from map_generator import generate_map
class GameEngine:
    """Owns the whole mutable state of one run of the game."""
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.level = 1
        self.player = Player(0, 0)   # position fixed by map generation below
        self.messages = []
        self.map_version = 0
        self.game_over = False
        self.last_monster = None      # stats of the most recently encountered monster
        self.monsters_defeated = 0
        self.chests_opened = 0
        self._build_level(first=True)
    # ------------------------------------------------------------------ #
    # Level handling
    # ------------------------------------------------------------------ #
    def _build_level(self, first=False):
        self.game_map = generate_map(self.level, self.rng)
        sx, sy = self.game_map.start
        if first:
            self.player = Player(sx, sy)
        else:
            self.player.move_to(sx, sy)
        self.map_version += 1
        self.log(f"Welcome to floor {self.level}." if first else f"You descend to floor {self.level}.")
        self.log("Reach the green door. W/A/S/D to move.")
    def _next_level(self):
        self.level += 1
        self.player.raise_max_hp(C.PLAYER_MAX_HP_PER_LEVEL)
        self.player.heal(C.PLAYER_MAX_HP_PER_LEVEL)  # small reward for descending
        self._build_level()