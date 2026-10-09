'''
game.py
Core game orchestration: application states (menu, playing, paused,
game over), the fixed-timestep game loop, input handling, scoring and
high-score persistence.
'''
import pygame
import settings
from snake import Snake
from food import Food
import ui
class Game:
    """Top-level application controller for the Snake game."""
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Snake - ChatDev Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = self.STATE_MENU
        self.high_score = ui.load_high_score()
        self.difficulty_names = list(settings.DIFFICULTIES.keys())
        self.selected_difficulty = self.difficulty_names.index(settings.DEFAULT_DIFFICULTY)
        self.snake = Snake(settings.GRID_WIDTH, settings.GRID_HEIGHT)
        self.food = Food(settings.GRID_WIDTH, settings.GRID_HEIGHT)
        self.score = 0
        self.move_interval = 1.0 / settings.DIFFICULTIES[settings.DEFAULT_DIFFICULTY]["speed"]
        self.move_timer = 0.0
        self.won = False
        self.new_record = False
    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def start_game(self):
        """Reset all gameplay state and begin a new round."""
        self.snake.reset()
        self.food.randomize_position(self.snake.body)
        self.score = 0
        self.won = False
        self.new_record = False
        name = self.difficulty_names[self.selected_difficulty]
        self.move_interval = 1.0 / settings.DIFFICULTIES[name]["speed"]
        self.move_timer = 0.0
        self.state = self.STATE_PLAYING
    def quit(self):
        self.running = False
    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
    def _handle_keydown(self, key):
        if self.state == self.STATE_MENU:
            if key in (pygame.K_UP, pygame.K_w):
                self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulty_names)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulty_names)
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()
            elif key == pygame.K_ESCAPE:
                self.quit()
        elif self.state == self.STATE_PLAYING:
            direction_map = {
                pygame.K_UP: settings.UP,    pygame.K_w: settings.UP,
                pygame.K_DOWN: settings.DOWN, pygame.K_s: settings.DOWN,
                pygame.K_LEFT: settings.LEFT, pygame.K_a: settings.LEFT,
                pygame.K_RIGHT: settings.RIGHT, pygame.K_d: settings.RIGHT,
            }
            if key in direction_map:
                self.snake.set_direction(direction_map[key])
            elif key == pygame.K_SPACE:
                self.state = self.STATE_PAUSED
            elif key == pygame.K_ESCAPE:
                self.state = self.STATE_MENU
        elif self.state == self.STATE_PAUSED:
            if key == pygame.K_SPACE:
                self.state = self.STATE_PLAYING
            elif key == pygame.K_m:
                self.state = self.STATE_MENU
            elif key == pygame.K_ESCAPE:
                self.quit()
        elif self.state == self.STATE_GAME_OVER:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()
            elif key == pygame.K_m:
                self.state = self.STATE_MENU
            elif key == pygame.K_ESCAPE:
                self.quit()
    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def _update(self, dt):
        if self.state != self.STATE_PLAYING:
            return
        self.move_timer += dt
        while self.move_timer >= self.move_interval:
            self.move_timer -= self.move_interval
            self._step()
    def _step(self):
        """Advance the simulation by exactly one grid cell."""
        new_head = self.snake.move()
        if self.snake.hits_boundary() or self.snake.hits_self():
            self._end_game()
            return
        if new_head == self.food.get_position():
            self.snake.grow()
            name = self.difficulty_names[self.selected_difficulty]
            self.score += settings.SCORE_PER_FOOD * settings.DIFFICULTIES[name]["multiplier"]
            if not self.food.randomize_position(self.snake.body):
                self.won = True          # board full -> player wins
                self._end_game()
    def _end_game(self):
        self.state = self.STATE_GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_record = True
            ui.save_high_score(self.high_score)
    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------
    def _render(self):
        if self.state == self.STATE_MENU:
            ui.draw_menu(self.screen, self.difficulty_names, self.selected_difficulty)
        else:
            ui.draw_board(self.screen, settings.GRID_HEIGHT * settings.GRID_SIZE)
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            name = self.difficulty_names[self.selected_difficulty]
            ui.draw_hud(self.screen, self.score, self.high_score, name,
                        self.state == self.STATE_PAUSED)
            if self.state == self.STATE_PAUSED:
                ui.draw_pause(self.screen)
            elif self.state == self.STATE_GAME_OVER:
                ui.draw_game_over(self.screen, self.score, self.high_score,
                                  self.new_record, self.won)
        pygame.display.flip()
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Run the application until the user quits."""
        while self.running:
            # Cap dt so that system stalls (e.g. window drag / sleep) cannot
            # cause the snake to jump many cells in a single frame.
            dt = min(self.clock.tick(settings.RENDER_FPS) / 1000.0, 0.1)
            self._handle_events()
            self._update(dt)
            self._render()
        pygame.quit()