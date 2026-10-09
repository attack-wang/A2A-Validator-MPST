'''
game.py
Core game state machine: movement, combat, pickups, level progression.
'''
import random
from settings import (
    GRID_WIDTH, GRID_HEIGHT, WALL, PLAYER_START_HP, LOG_LINES,
)
from pathfinding import DIRS4
from entities import Player
from map_generator import MapGenerator
MOVE_KEYS = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}
class Game:
    '''Holds all mutable game state and resolves one player action at a time.'''
    def __init__(self):
        self.level = 1
        self.rng = random.Random()
        self.generator = MapGenerator(self.rng)
        self.messages = []          # list of (text, kind) log entries
        self.game_over = False
        self.player = None
        self.floor_version = 0      # bumped on every floor (re)load
        self._load_floor(keep_hp=False)
        self._log("Climb the tower. Reach the golden door!", "info")
    # ------------------------------------------------------------------ floor
    def _load_floor(self, keep_hp):
        fm = self.generator.generate(self.level)
        self.grid = fm.grid
        self.door = fm.door
        self.monsters = {(m.x, m.y): m for m in fm.monsters}
        self.chests = {(c.x, c.y): c for c in fm.chests}
        if keep_hp and self.player is not None:
            hp = self.player.hp
        else:
            hp = PLAYER_START_HP
        self.player = Player(fm.start[0], fm.start[1], hp)
        self.last_monster = None    # last monster fought (for the UI)
        self.nearby_monster = None  # monster adjacent to the player (for the UI)
        self.floor_version += 1
        self._update_nearby()
    # ------------------------------------------------------------------ input
    def handle_input(self, key):
        '''Apply a WASD move. Returns True when the game state changed.'''
        if self.game_over or key not in MOVE_KEYS:
            return False
        self._try_move(*MOVE_KEYS[key])
        return True
    def _try_move(self, dx, dy):
        nx = self.player.x + dx
        ny = self.player.y + dy
        if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
            return
        if self.grid[ny][nx] == WALL:
            self._log("The wall blocks your way.", "info")
            return
        self.player.x, self.player.y = nx, ny
        if (nx, ny) == self.door:
            self._next_level()
            return
        if (nx, ny) in self.chests:
            chest = self.chests.pop((nx, ny))
            self.player.hp += chest.heal
            self._log(f"You open a chest and recover {chest.heal} HP.", "good")
        if (nx, ny) in self.monsters:
            self._fight(self.monsters[(nx, ny)])
        self._update_nearby()
    # ---------------------------------------------------- combat / progression
    def _fight(self, monster):
        damage = monster.hp
        self.player.hp -= damage
        self.last_monster = monster
        self.monsters.pop((monster.x, monster.y), None)
        self._log(f"You fought the {monster.name} and lost {damage} HP.", "danger")
        if self.player.hp <= 0:
            self.player.hp = 0
            self.game_over = True
            self._log("You have fallen... Press R to restart.", "danger")
    def _next_level(self):
        self.level += 1
        self._load_floor(keep_hp=True)
        self._log(f"You ascend to floor {self.level}.", "good")
    def restart(self):
        self.level = 1
        self.game_over = False
        self.messages = []
        self._load_floor(keep_hp=False)
        self._log("A new climb begins. Reach the door!", "info")
    # ----------------------------------------------------------------- helpers
    def _update_nearby(self):
        '''Remember a 4-directionally adjacent monster for the sidebar UI.'''
        self.nearby_monster = None
        if self.player is None:
            return
        for dx, dy in DIRS4:
            monster = self.monsters.get((self.player.x + dx, self.player.y + dy))
            if monster is not None:
                self.nearby_monster = monster
                return
    def _log(self, text, kind="info"):
        self.messages.append((text, kind))
        if len(self.messages) > LOG_LINES:
            del self.messages[:-LOG_LINES]