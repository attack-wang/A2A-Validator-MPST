'''
game.py
Core game engine: manages the game loop, event handling,
state updates, collision checks, scoring, and rendering.
The loop renders at BASE_FPS while the snake advances on a
fixed interval determined by the chosen difficulty speed.
'''
import sys
import pygame
import settings
from snake import Snake
from food import Food
import ui
class Game:
    """Encapsulates a full Snake game session."""
    def __init__(self, difficulty_name):
        """Initialize a game session for the given difficulty."""
        self.difficulty_name = difficulty_name
        self.speed = settings.DIFFICULTY_SETTINGS[difficulty_name]["speed"]
        self.snake = Snake()
        self.food = Food()
        self.food.randomize_position(self.snake.get_body())
        self.score = 0
        self.game_over = False
        self.victory = False
        self.quit_to_menu = False
        self.paused = False
        self.clock = pygame.time.Clock()
        self.move_timer = 0.0                    # ms accumulated since last move
        self.move_interval = 1000 / self.speed   # ms per snake move
    def handle_events(self):
        """Process pygame events: quit, direction keys, pause, ESC to menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.snake.set_direction(settings.UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.set_direction(settings.DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.set_direction(settings.LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.set_direction(settings.RIGHT)
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    self.quit_to_menu = True
    def step(self):
        """One logical move of the snake: move, collide-check, eat."""
        self.snake.update()
        # Boundary collision
        head_x, head_y = self.snake.get_head_position()
        if not (0 <= head_x < settings.GRID_WIDTH and 0 <= head_y < settings.GRID_HEIGHT):
            self.game_over = True
            return
        # Self collision
        if self.snake.check_self_collision():
            self.game_over = True
            return
        # Food eating
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.score += 1
            self.food.randomize_position(self.snake.get_body())
            if self.food.position is None:
                self.victory = True  # board completely filled
    def render(self, screen):
        """Draw one full frame (plus pause overlay if needed) and flip it."""
        ui.render_game(screen, self)
        if self.paused:
            ui.draw_pause_overlay(screen)
        pygame.display.flip()
    def run(self, screen):
        """
        Main game loop. Returns 'menu' if the player pressed ESC,
        or 'finished' when the game ends (game over or victory).
        """
        while True:
            delta_ms = self.clock.tick(settings.BASE_FPS)
            self.handle_events()
            if self.quit_to_menu:
                return "menu"
            if self.game_over or self.victory:
                return "finished"
            if not self.paused:
                self.move_timer += delta_ms
                while self.move_timer >= self.move_interval:
                    self.move_timer -= self.move_interval
                    self.step()
                    if self.game_over or self.victory:
                        break
            self.render(screen)