'''
game.py
Core game logic: state, input handling, movement, combat resolution,
treasure chests, level transitions and held-key repeat movement.
Deliberately free of pygame calls except for the key-constant mapping,
so the rules are easy to test headlessly.
'''
import random
import pygame  # only for key constants
import config
from entities import Player
from map_generator import MapGenerator
class Game:
    """Holds the whole game state and applies the rules to player input."""
    MOVES = {
        pygame.K_w: (0, -1),   # up
        pygame.K_a: (-1, 0),   # left
        pygame.K_s: (0, 1),    # down
        pygame.K_d: (1, 0),    # right
    }
    def __init__(self):
        self.generator = MapGenerator()
        self.level = 1
        self.player = None
        self.game_map = None
        self.log = []
        self.state = "playing"          # "playing" | "dead"
        self.last_monster_info = None   # (name, hp) of the last fought monster
        self._held = {}                 # key -> ms elapsed since last repeat
        self._last_blocked = None       # throttle "blocked by wall" spam
        self.start_level()
    # -- level lifecycle ----------------------------------------------------
    def start_level(self):
        """Generate the current level and (re)place the player, keeping HP."""
        hp = self.player.hp if self.player else config.PLAYER_START_HP
        self.game_map = self.generator.generate(self.level)
        self.player = Player(self.game_map.start[0], self.game_map.start[1], hp)
        self._last_blocked = None
        self.add_log(f"-- Level {self.level} --  Find the door. HP: {self.player.hp}")
    def restart(self):
        """Full reset after death."""
        self.level = 1
        self.player = None
        self.log = []
        self.last_monster_info = None
        self.state = "playing"
        self._held.clear()
        self.start_level()
    def add_log(self, message):
        self.log.append(message)
        if len(self.log) > config.MAX_LOG_LINES:
            self.log = self.log[-config.MAX_LOG_LINES:]
    # -- input --------------------------------------------------------------
    def handle_keydown(self, key):
        """Apply one key press. Returns True if the game state changed."""
        if self.state == "dead":
            if key == pygame.K_r:
                self.restart()
                return True
            return False
        delta = self.MOVES.get(key)
        if delta is None:
            return False
        return self._try_move(*delta)
    def press_key(self, key):
        """Register a key as held (for repeat movement)."""
        if key in self.MOVES and self.state == "playing":
            self._held[key] = 0.0
    def release_key(self, key):
        """Forget a released key."""
        self._held.pop(key, None)
    def update_held_keys(self, dt_ms):
        """Repeat movement for keys held longer than MOVE_REPEAT_MS."""
        if self.state != "playing":
            self._held.clear()
            return
        for key in list(self._held.keys()):
            self._held[key] += dt_ms
            if self._held[key] >= config.MOVE_REPEAT_MS:
                self._held[key] = 0.0
                self.handle_keydown(key)
    # -- movement / rules ---------------------------------------------------
    def _try_move(self, dx, dy):
        nx, ny = self.player.x + dx, self.player.y + dy
        if not self.game_map.is_floor(nx, ny):
            if (nx, ny) != self._last_blocked:   # avoid log spam against walls
                self.add_log("Blocked by a wall.")
                self._last_blocked = (nx, ny)
            return False
        self._last_blocked = None
        monster = self.game_map.monster_at(nx, ny)
        if monster is not None:
            return self._fight(monster, nx, ny)
        chest = self.game_map.chest_at(nx, ny)
        if chest is not None:
            healed = self.player.heal(chest.open())
            self.game_map.remove_chest(chest)
            self.player.move_to(nx, ny)
            self.add_log(f"Opened a chest: +{healed} HP (now {self.player.hp}).")
            return True
        self.player.move_to(nx, ny)
        if (nx, ny) == self.game_map.door:
            self.level += 1
            self.add_log("You found the door! Descending...")
            self.start_level()
        return True
    def _fight(self, monster, nx, ny):
        """Combat: the monster's HP is subtracted from the player's HP."""
        damage = monster.hp
        self.player.take_damage(damage)
        self.last_monster_info = (monster.name, monster.hp)
        self.game_map.remove_monster(monster)
        monster.defeat()
        if not self.player.is_alive():
            self.state = "dead"
            self._held.clear()
            self.add_log(f"The {monster.name} (HP {damage}) killed you!")
            return True
        self.player.move_to(nx, ny)
        self.add_log(f"Fought {monster.name} (HP {damage}): -{damage} HP (now {self.player.hp}).")
        return True
    # -- UI helpers ---------------------------------------------------------
    def adjacent_monsters(self):
        """Monsters in the 4 tiles next to the player, for the sidebar UI."""
        px, py = self.player.position
        result = []
        for dx, dy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            monster = self.game_map.monster_at(px + dx, py + dy)
            if monster is not None:
                result.append(monster)
        return result