'''
game.py
Core game state and rules: level loading, W/A/S/D movement with wall
collision, combat resolution, chest healing, door progression and the
message log consumed by the UI.
'''
import pygame
import config
from entities import Player
from map_generator import MapGenerator
class Game:
    def __init__(self):
        self.level_number = 1
        self.messages = []
        self.game_over = False
        self.player = Player(0, 0, config.PLAYER_START_HP)
        self.grid = None
        self.door = None
        self.monsters = {}
        self.chests = {}
        self._load_level(1, keep_hp=False)
    # ------------------------------------------------------------------ #
    # Level management
    # ------------------------------------------------------------------ #
    def _load_level(self, level, keep_hp):
        data = MapGenerator().generate_level(level)
        self.grid = data.grid
        self.door = data.door
        self.monsters = {(m.x, m.y): m for m in data.monsters}
        self.chests = {(c.x, c.y): c for c in data.chests}
        if not keep_hp:
            self.player.hp = config.PLAYER_START_HP
        self.player.x, self.player.y = data.start
        self.level_number = level
        self.log(f"Welcome to floor {level}!", config.COLOR_MESSAGE_LEVEL)
    def _next_level(self):
        self._load_level(self.level_number + 1, keep_hp=True)
    def restart(self):
        self.game_over = False
        self.messages = []
        self._load_level(1, keep_hp=False)
    # ------------------------------------------------------------------ #
    # Input / movement
    # ------------------------------------------------------------------ #
    def handle_key(self, key):
        if self.game_over:
            if key == pygame.K_r:
                self.restart()
            return
        direction = {
            pygame.K_w: (0, -1),
            pygame.K_a: (-1, 0),
            pygame.K_s: (0, 1),
            pygame.K_d: (1, 0),
        }.get(key)
        if direction:
            self.try_move(*direction)
    def try_move(self, dx, dy):
        if self.game_over:
            return
        nx, ny = self.player.x + dx, self.player.y + dy
        if not (0 <= nx < config.GRID_SIZE and 0 <= ny < config.GRID_SIZE):
            return
        if self.grid[ny][nx] != config.TILE_FLOOR:
            return  # walls block movement
        monster = self.monsters.pop((nx, ny), None)
        if monster:
            self.player.hp -= monster.hp
            self.log(f"Fought {monster.name} (HP {monster.hp})! -{monster.hp} HP",
                     config.COLOR_MESSAGE_COMBAT)
            if self.player.hp <= 0:
                self.player.hp = 0
                self.game_over = True
                self.log("You died... Press R to restart.", config.COLOR_MESSAGE_COMBAT)
                return
        chest = self.chests.pop((nx, ny), None)
        if chest:
            self.player.hp += chest.heal_amount
            self.log(f"Treasure chest! +{chest.heal_amount} HP",
                     config.COLOR_MESSAGE_HEAL)
        self.player.x, self.player.y = nx, ny
        if (nx, ny) == self.door.position:
            self.log(f"You reached the door! Descending to floor {self.level_number + 1}...",
                     config.COLOR_MESSAGE_LEVEL)
            self._next_level()
    # ------------------------------------------------------------------ #
    # Misc
    # ------------------------------------------------------------------ #
    def update(self):
        pass  # turn-based; kept as no-op because main.py calls it
    def log(self, text, color=None):
        self.messages.append((text, color))
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]
    def adjacent_monsters(self):
        """Monsters on the 4 tiles next to the player (for the stats UI)."""
        result = []
        px, py = self.player.x, self.player.y
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            monster = self.monsters.get((px + dx, py + dy))
            if monster:
                result.append(monster)
        return result