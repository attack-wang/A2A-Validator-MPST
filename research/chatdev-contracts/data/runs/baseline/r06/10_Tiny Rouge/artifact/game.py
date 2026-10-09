'''
game.py
Core game logic: level flow, player movement, combat, chests, and the main loop.
'''
import pygame
import config
from entities import Player
from map_generator import MapGenerator
from ui import UI
class Game:
    """Top-level game object owning state, the event/update/render loop."""
    DIRECTIONS = {
        pygame.K_w: (0, -1),
        pygame.K_a: (-1, 0),
        pygame.K_s: (0, 1),
        pygame.K_d: (1, 0),
    }
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 110)  # allow held-key movement
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("Tower of the Sorcerer")
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.generator = MapGenerator()
        self.messages = []
        self.running = True
        self.game_over = False
        self.level = 1
        self.map_version = 0   # bumped every time a new map is built (UI cache key)
        self.player = None
        self.map_data = None
        self.encountered = []  # monsters adjacent to the player (for the UI)
        self._start_level()
    # --- level flow -------------------------------------------------
    def _start_level(self):
        self.map_data = self.generator.generate(self.level)
        self.map_version += 1
        sx, sy = self.map_data.start
        if self.player is None:
            self.player = Player(sx, sy, config.PLAYER_START_HP)
        else:
            self.player.move_to(sx, sy)
        self.encountered = []
        self._update_encountered()
        self._log(f"-- Descended to floor {self.level} --")
    def _next_level(self):
        self.level += 1
        self._start_level()
    def _restart(self):
        self.level = 1
        self.player = None
        self.game_over = False
        self.messages = []
        self._start_level()
    def _log(self, text):
        self.messages.append(text)
        if len(self.messages) > 6:
            self.messages.pop(0)
    # --- input & movement -------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key == pygame.K_r:
                    self._restart()
                return
            delta = self.DIRECTIONS.get(event.key)
            if delta:
                self._try_move(*delta)
    def _try_move(self, dx, dy):
        nx, ny = self.player.x + dx, self.player.y + dy
        if not (0 <= nx < config.GRID_SIZE and 0 <= ny < config.GRID_SIZE):
            return
        tile = self.map_data.grid[ny][nx]
        if tile == config.WALL:
            return  # cannot pass through walls
        pos = (nx, ny)
        monster = self.map_data.monsters.get(pos)
        if monster is not None:
            self._combat(monster, pos)
            return
        chest = self.map_data.chests.get(pos)
        if chest is not None:
            del self.map_data.chests[pos]
            heal = chest.heal_amount
            self.player.heal(heal)
            self._log(f"Opened a chest: +{heal} HP (HP {self.player.hp}).")
        self.player.move_to(nx, ny)
        if tile == config.DOOR:
            self._log("You found the door! Descending...")
            self._next_level()
        else:
            self._update_encountered()
    def _combat(self, monster, pos):
        """Combat: the monster's HP is subtracted from the player's HP."""
        self.player.take_damage(monster.hp)
        del self.map_data.monsters[pos]
        self._log(f"Fought {monster.name} (-{monster.hp} HP). HP {max(self.player.hp, 0)}.")
        if not self.player.is_alive():
            self.player.hp = 0
            self.game_over = True
            self._log("You died! Press R to restart.")
        else:
            self._update_encountered()
    def _update_encountered(self):
        """Monsters on the four tiles adjacent to the player are 'encountered'."""
        found = []
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            m = self.map_data.monsters.get((self.player.x + dx, self.player.y + dy))
            if m:
                found.append(m)
        self.encountered = found
    # --- main loop ---------------------------------------------------
    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.ui.draw(self.screen, self)
            pygame.display.flip()
            self.clock.tick(config.FPS)
        pygame.quit()