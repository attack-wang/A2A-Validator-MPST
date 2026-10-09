'''Core game loop: input handling, movement, combat, progression and rendering.'''
import pygame
import settings
from entities import Player
from map_generator import generate_level
from ui import UI
class Game:
    '''Coordinates the tower floors, the player and the rendering/UI.'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption("Tower of the Sorcerer")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.level = 1
        self.state = "playing"      # playing / dead / victory
        self.messages = []
        self.last_monster = None
        self._load_level(self.level)
    def _load_level(self, level):
        '''Generate a new floor and reset the player on its start tile.'''
        (self.grid, self.start, self.door,
         self.monsters, self.chests) = generate_level(level)
        self.player = Player(self.start[0], self.start[1])
        self.messages = [f"Welcome to floor {level}!"]
    def run(self):
        '''Main loop: pump events, update, draw at the configured FPS.'''
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_key(event.key)
            self.ui.draw(self)
            pygame.display.flip()
            self.clock.tick(settings.FPS)
        pygame.quit()
    def _handle_key(self, key):
        '''React to W/A/S/D (or arrow) movement, or restart after death/win.'''
        if self.state != "playing":
            if key in (pygame.K_r, pygame.K_SPACE):
                self.level = 1
                self.state = "playing"
                self.last_monster = None
                self._load_level(self.level)
            return
        moves = {
            pygame.K_w: (0, -1), pygame.K_UP: (0, -1),
            pygame.K_a: (-1, 0), pygame.K_LEFT: (-1, 0),
            pygame.K_s: (0, 1), pygame.K_DOWN: (0, 1),
            pygame.K_d: (1, 0), pygame.K_RIGHT: (1, 0),
        }
        if key in moves:
            dx, dy = moves[key]
            self._try_move(dx, dy)
    def _try_move(self, dx, dy):
        '''Attempt to move the player one tile; walls are impassable.'''
        nx, ny = self.player.x + dx, self.player.y + dy
        if not (0 <= nx < settings.GRID_SIZE and 0 <= ny < settings.GRID_SIZE):
            return
        if self.grid[ny][nx] == settings.WALL:
            return
        self.player.x, self.player.y = nx, ny
        self._resolve_tile(nx, ny)
    def _resolve_tile(self, x, y):
        '''Handle monster combat, chest pickup or door transition on new tile.'''
        pos = (x, y)
        if pos in self.monsters:
            monster = self.monsters.pop(pos)
            self.last_monster = monster
            damage = monster.hp         # combat: lose HP equal to monster HP
            self.player.take_damage(damage)
            self.messages.append(f"Fought {monster.name} (-{damage} HP)")
            if not self.player.is_alive():
                self.player.hp = 0
                self.state = "dead"
                self.messages.append("You died! Press R to restart.")
            return
        if pos in self.chests:
            chest = self.chests.pop(pos)
            self.player.heal(chest.heal_amount)
            self.messages.append(f"Opened a chest (+{chest.heal_amount} HP)")
            return
        if pos == self.door:
            if self.level >= settings.MAX_LEVELS:
                self.state = "victory"
                self.messages.append("You conquered the tower! Press R to restart.")
            else:
                self.level += 1
                self._load_level(self.level)