'''
game.py
Game class: application loop, state management, scoring, and difficulty selection.
'''
import pygame
from settings import (WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS, BLACK, WHITE,
                      GRAY, YELLOW, GREEN, RED, BLUE,
                      UP, DOWN, LEFT, RIGHT, DIFFICULTY_LEVELS)
from snake import Snake
from food import Food
from ui import draw_text, draw_grid
class Game:
    """Classic Snake game with menu, playing, and game-over states."""
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        """Initialize pygame, the window, clock, entities, and game state."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Classic Snake")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = Game.STATE_MENU
        self.difficulty = "Medium"
        self.score = 0
        self.high_score = 0
        self.won = False
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.move_timer = 0
        self.move_interval = 1000 / DIFFICULTY_LEVELS[self.difficulty]["speed"]
    def run(self):
        """Main application loop with a graceful exit path."""
        while self.running:
            delta_ms = self.clock.tick(MAX_FPS)
            self.handle_events()
            if self.state == Game.STATE_PLAYING:
                self.move_timer += delta_ms
                while (self.move_timer >= self.move_interval
                       and self.state == Game.STATE_PLAYING):
                    self.move_timer -= self.move_interval
                    self.step()
            self.render()
        pygame.quit()
    def handle_events(self):
        """Dispatch pygame events to the state-specific key handler."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    def handle_keydown(self, key):
        """Route key presses according to the current game state."""
        if self.state == Game.STATE_MENU:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()
            elif key == pygame.K_LEFT:
                self.cycle_difficulty(-1)
            elif key == pygame.K_RIGHT:
                self.cycle_difficulty(1)
            elif key == pygame.K_ESCAPE:
                self.running = False
        elif self.state == Game.STATE_PLAYING:
            mapping = {pygame.K_UP: UP, pygame.K_w: UP,
                       pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
                       pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
                       pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT}
            if key in mapping:
                self.snake.change_direction(mapping[key])
        else:  # STATE_GAME_OVER
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = Game.STATE_MENU
            elif key == pygame.K_ESCAPE:
                self.running = False
    def cycle_difficulty(self, step):
        """Move the difficulty selection forward/backward through levels."""
        names = list(DIFFICULTY_LEVELS)
        self.difficulty = names[(names.index(self.difficulty) + step) % len(names)]
    def start_game(self):
        """Reset entities and timing, then switch to the playing state."""
        self.snake.reset()
        self.food.randomize_position(self.snake.body)
        self.score = 0
        self.won = False
        self.move_interval = 1000 / DIFFICULTY_LEVELS[self.difficulty]["speed"]
        self.move_timer = 0
        self.state = Game.STATE_PLAYING
    def step(self):
        """Advance the simulation by one grid cell."""
        if not self.snake.update():
            self.end_game(won=False)
            return
        if self.snake.head == self.food.get_position():
            self.score += DIFFICULTY_LEVELS[self.difficulty]["multiplier"]
            self.snake.grow_pending += 1
            self.food.randomize_position(self.snake.body)
            if self.food.get_position() is None:
                self.end_game(won=True)  # board completely filled
    def end_game(self, won):
        """Record the result and switch to the game-over state."""
        self.won = won
        self.high_score = max(self.high_score, self.score)
        self.state = Game.STATE_GAME_OVER
    def render(self):
        """Draw the current frame based on the game state."""
        self.screen.fill(BLACK)
        if self.state == Game.STATE_MENU:
            self.render_menu()
        else:
            draw_grid(self.screen)
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            draw_text(self.screen, f"Score: {self.score}", 26, WHITE, topleft=(10, 8))
            draw_text(self.screen, f"High: {self.high_score}", 20, GRAY, topleft=(10, 40))
            draw_text(self.screen, f"Level: {self.difficulty}", 20, BLUE,
                      center=(WINDOW_WIDTH - 80, 20))
            if self.state == Game.STATE_GAME_OVER:
                self.render_game_over()
        pygame.display.flip()
    def render_menu(self):
        """Draw the title screen with difficulty selection."""
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        draw_text(self.screen, "CLASSIC SNAKE", 52, GREEN, center=(cx, cy - 90))
        draw_text(self.screen, f"< {self.difficulty} >", 32, YELLOW, center=(cx, cy - 10))
        draw_text(self.screen, "LEFT/RIGHT: difficulty   ENTER: start", 22, WHITE, center=(cx, cy + 50))
        draw_text(self.screen, "Arrows/WASD to move  -  ESC to quit", 20, GRAY, center=(cx, cy + 90))
        draw_text(self.screen, f"High score: {self.high_score}", 22, YELLOW, center=(cx, cy + 140))
    def render_game_over(self):
        """Draw the game-over/win overlay with the final score."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        draw_text(self.screen, "YOU WIN!" if self.won else "GAME OVER", 52,
                  YELLOW if self.won else RED, center=(cx, cy - 40))
        draw_text(self.screen, f"Final score: {self.score}", 30, WHITE, center=(cx, cy + 20))
        draw_text(self.screen, "ENTER: menu   ESC: quit", 22, GRAY, center=(cx, cy + 70))