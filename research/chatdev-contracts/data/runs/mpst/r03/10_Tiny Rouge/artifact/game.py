'''
game.py
Core game state and rules: movement, combat, treasure pickup, level flow.
'''
from collections import deque
import settings
from entities import Player
from map_generator import MapGenerator
class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.level = 1
        self.player = Player(1, 1)
        self.state = "playing"   # "playing" | "game_over"
        self.messages = deque(maxlen=6)
        self.encountered_monster = None  # dict with last combat info
        self.static_changed = True  # flag for renderer cache
        self.build_level()
    def build_level(self):
        gen = MapGenerator(level=self.level, rng=self.rng)
        data = gen.generate()
        self.grid = data["grid"]
        self.door = data["door"]
        self.monsters = data["monsters"]
        self.treasures = data["treasures"]
        self.player.x, self.player.y = data["start"]
        self.encountered_monster = None
        self.static_changed = True
        self.add_message(f"Welcome to floor {self.level}!")
    # helpers -------------------------------------------------------------
    def tile_at(self, x, y):
        return self.grid[y][x]
    def monster_at(self, x, y):
        for m in self.monsters:
            if m.x == x and m.y == y:
                return m
        return None
    def treasure_at(self, x, y):
        for t in self.treasures:
            if t.x == x and t.y == y:
                return t
        return None
    def add_message(self, text):
        self.messages.appendleft(text)  # newest first? or append