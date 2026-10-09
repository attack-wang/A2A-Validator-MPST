'''
game.py
Game core: main loop, input handling, movement, combat, chests and level flow.
'''
import sys
import pygame
import settings
from entities import Player
from map_generator import MapGenerator
from ui import UI
MOVE_KEYS = {
    pygame.K_w: (0, -1),
    pygame.K_a: (-1, 0),
    pygame.K_s: (0, 1),
    pygame.K_d: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_DOWN: (0, 1),
    pygame.K_RIGHT: (1, 0),
}
class Game:
    """Owns the pygame window, the current level and the game state machine."""
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.generator = MapGenerator()
        self.messages = []
        self.running = True
        self._start_level(1)
    def _start_level(self, number):
        """Generate a new floor and reset transient state."""
        self.level = self.generator.generate(number)
        self.player = Player(self.level.start[0], self.level.start[1])
        self.game_over = False
        self.messages = [f"Welcome to floor {number}."]
    def run(self):
        """Main loop: pump events, update, render, tick."""
        while self.running:
            self._handle_events()
            self._render()
            self.clock.tick(settings.FPS)
        pygame.quit()
    def _handle_events(self):
        """Process quit, movement, restart and exit keys."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS and not self.game_over:
                    self._try_move(*MOVE_KEYS[event.key])
                elif event.key == pygame.K_r and self.game_over:
                    self._start_level(1)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    def _try_move(self, dx, dy):
        """Attempt one grid step; resolve chest, monster and door interactions."""
        if self.game_over:
            return
        nx, ny = self.player.x + dx, self.player.y + dy
        if not self.level.in_bounds(nx, ny) or self.level.is_wall(nx, ny):
            return  # walls block movement
        chest = self.level.chest_at(nx, ny)
        if chest is not None:
            healed = self.player.heal(chest.heal_amount)
            self.level.remove_chest(chest)
            self.messages.append(f"Opened a chest: +{healed} HP.")
        monster = self.level.monster_at(nx, ny)
        if monster is not None:
            self.player.take_damage(monster.hp)  # combat: subtract monster HP
            self.messages.append(f"{monster.name} hits you for {monster.hp}!")
            if self.player.is_dead:
                self.player.hp = 0
                self.game_over = True
                self.messages.append("You died...")
                return
            self.level.remove_monster(monster)
        self.player.x, self.player.y = nx, ny
        if self.level.is_door(nx, ny):
            self._next_level()
    def _next_level(self):
        """Descend through the door to the next floor."""
        self._start_level(self.level.number + 1)
    def _nearby_monsters(self):
        """Monsters adjacent (8-directional) to the player, for the UI panel."""
        result = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                monster = self.level.monster_at(self.player.x + dx, self.player.y + dy)
                if monster is not None:
                    result.append(monster)
        return result
    def _render(self):
        """Draw the current frame."""
        self.ui.draw_game(self.screen, self.level, self.player,
                          self._nearby_monsters(), self.messages, self.game_over)
        pygame.display.flip()