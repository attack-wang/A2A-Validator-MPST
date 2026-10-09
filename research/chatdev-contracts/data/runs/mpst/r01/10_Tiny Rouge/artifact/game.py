'''
game.py
Core game logic and main loop for the Tower of the Sorcerer roguelike.
Owns the pygame window, the Player and the current Level.  Implements
WASD movement (up/left/down/right), wall blocking, combat resolution
(monster HP is subtracted from the player's HP), treasure chest healing
(20-30 HP), door progression to the next floor, game over on death and
restart with the R key.
'''
import random
from collections import deque
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE,
    PLAYER_START_HP, CHEST_HEAL_MIN, CHEST_HEAL_MAX, MAX_MESSAGES,
)
from entities import Player
from level import Level
from ui import UI
class Game:
    """Ties together input, game rules, level progression and rendering."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.rng = random.Random()
        self.messages = deque(maxlen=MAX_MESSAGES)
        self.ui = UI(self.screen)
        self.running = True
        self.game_over = False
        self.player = None
        self.level = None
        self.tower_level = 1
        self.new_game()
    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def new_game(self):
        """(Re)start a run: fresh player, back to floor 1."""
        self.tower_level = 1
        self.player = Player(0, 0, PLAYER_START_HP)
        self.game_over = False
        self.messages.clear()
        self.load_level(1)
        self.log("Welcome to the Tower of the Sorcerer!")
    def load_level(self, number):
        """Generate floor `number` and place the player at its start."""
        self.level = Level(number, self.rng)
        self.player.move_to(*self.level.start)
        self.log(f"-- Floor {number} --")
    def log(self, text):
        self.messages.append(text)
    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.new_game()
                elif not self.game_over:
                    if event.key == pygame.K_w:      # up
                        self.attempt_move(0, -1)
                    elif event.key == pygame.K_a:    # left
                        self.attempt_move(-1, 0)
                    elif event.key == pygame.K_s:    # down
                        self.attempt_move(0, 1)
                    elif event.key == pygame.K_d:    # right
                        self.attempt_move(1, 0)
    # ------------------------------------------------------------------
    # Movement / interaction rules
    # ------------------------------------------------------------------
    def attempt_move(self, dx, dy):
        """Try to move the player one tile; blocked by walls, fights
        monsters, opens chests and uses doors."""
        if self.game_over:
            return
        nx = self.player.x + dx
        ny = self.player.y + dy
        if self.level.is_wall(nx, ny):
            return  # walls are impassable
        monster = self.level.monster_at(nx, ny)
        if monster is not None:
            self.resolve_combat(monster)
            return
        if self.level.chest_at(nx, ny):
            self.open_chest(nx, ny)
            return
        if self.level.is_door(nx, ny):
            self.enter_door()
            return
        self.player.move_to(nx, ny)
    def resolve_combat(self, monster):
        """Combat: the monster's HP is subtracted from the player's HP."""
        damage = monster.hp
        self.player.take_damage(damage)
        if not self.player.is_alive():
            self.player.hp = 0
            self.game_over = True
            self.log(f"You were slain by the {monster.name}! (-{damage} HP)")
        else:
            self.level.remove_monster(monster.x, monster.y)
            self.player.move_to(monster.x, monster.y)
            self.log(f"You defeated the {monster.name}! (-{damage} HP)")
    def open_chest(self, x, y):
        """Treasure chests restore a random 20-30 HP."""
        heal = self.rng.randint(CHEST_HEAL_MIN, CHEST_HEAL_MAX)
        self.player.heal(heal)
        self.level.remove_chest(x, y)
        self.player.move_to(x, y)
        self.log(f"Treasure chest! Restored {heal} HP.")
    def enter_door(self):
        """Reaching the door leads to the next floor of the tower."""
        self.tower_level += 1
        self.load_level(self.tower_level)
        self.log(f"You descend to floor {self.tower_level}!")
    def adjacent_monsters(self):
        """Monsters on the tiles surrounding the player, for the HUD."""
        found = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                monster = self.level.monster_at(self.player.x + dx,
                                                self.player.y + dy)
                if monster is not None:
                    found.append(monster)
        return found
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            self.handle_input(pygame.event.get())
            self.ui.draw(self)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()