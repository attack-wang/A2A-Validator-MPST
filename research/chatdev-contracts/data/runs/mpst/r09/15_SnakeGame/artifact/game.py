'''
game.py
Game orchestration module for the Classic Snake game.
Defines the complete Game class: pygame window setup, state machine
(menu / playing / game over), fixed-timestep simulation loop,
keyboard input handling, scoring, highscore persistence and rendering.
'''
import json
import sys
import pygame
import settings
from food import Food
from snake import Snake
from ui import draw_text, draw_overlay
class Game:
    """Owns the pygame window, the game state and the main loop."""
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Classic Snake")
        self.clock = pygame.time.Clock()
        self.highscore = self._load_highscore()
        self.difficulty_key = "2"
        self.state = self.STATE_MENU
        self.reset()
    # ------------------------------------------------------------------
    # Highscore persistence
    # ------------------------------------------------------------------
    def _load_highscore(self):
        """Read the persisted highscore; return 0 when unavailable."""
        try:
            with open(settings.HIGHSCORE_FILE, "r", encoding="utf-8") as fh:
                return int(json.load(fh).get("highscore", 0))
        except (OSError, ValueError, TypeError):
            return 0
    def _save_highscore(self):
        """Persist the current highscore, ignoring write errors."""
        try:
            with open(settings.HIGHSCORE_FILE, "w", encoding="utf-8") as fh:
                json.dump({"highscore": self.highscore}, fh)
        except OSError:
            pass
    # ------------------------------------------------------------------
    # Round lifecycle
    # ------------------------------------------------------------------
    def reset(self):
        """Initialise a fresh round for the selected difficulty."""
        preset = settings.DIFFICULTIES[self.difficulty_key]
        self.speed = float(preset["speed"])
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self.move_accumulator = 0.0
        self.won = False
    def start(self, difficulty_key):
        """Start a new round with the given difficulty preset key."""
        self.difficulty_key = difficulty_key
        self.reset()
        self.state = self.STATE_PLAYING
    def _end_round(self, won):
        """Switch to the game-over state and persist a new highscore."""
        self.won = won
        self.state = self.STATE_GAME_OVER
        if self.score > self.highscore:
            self.highscore = self.score
            self._save_highscore()
    # ------------------------------------------------------------------
    # Simulation
    # ------------------------------------------------------------------
    def step(self):
        """Advance the simulation by exactly one grid move."""
        direction = self.snake.peek_direction()
        hx, hy = self.snake.head()
        next_head = (hx + direction[0], hy + direction[1])
        # Grow *before* moving so the tail stays put on the eating move.
        if self.food.position == next_head:
            self.snake.grow()
        head = self.snake.move()
        if self._out_of_bounds(head) or self.snake.hits_self():
            self._end_round(won=False)
            return
        if head == self.food.position:
            self.score += settings.SCORE_PER_FOOD
            self.speed = min(self.speed + settings.SPEED_INCREMENT,
                             settings.MAX_SPEED)
            self.food.respawn(self.snake)
            if self.food.position is None:  # board completely filled
                self._end_round(won=True)
    def _out_of_bounds(self, cell):
        """True when `cell` lies outside the board."""
        x, y = cell
        return not (0 <= x < settings.BOARD_WIDTH
                    and 0 <= y < settings.BOARD_HEIGHT)
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Run the game until the user quits."""
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self._handle_events()
            if self.state == self.STATE_PLAYING:
                self.move_accumulator += dt
                interval = 1.0 / self.speed
                while self.move_accumulator >= interval:
                    self.move_accumulator -= interval
                    self.step()
            self._render()
            pygame.display.flip()
    def _handle_events(self):
        """Process the pygame event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._on_keydown(event.key)
    def _on_keydown(self, key):
        """Dispatch KEYDOWN events depending on the current state."""
        if self.state == self.STATE_MENU:
            if key in (pygame.K_1, pygame.K_KP1):
                self.start("1")
            elif key in (pygame.K_2, pygame.K_KP2):
                self.start("2")
            elif key in (pygame.K_3, pygame.K_KP3):
                self.start("3")
        elif self.state == self.STATE_PLAYING:
            direction_map = {
                pygame.K_UP: settings.UP,
                pygame.K_w: settings.UP,
                pygame.K_DOWN: settings.DOWN,
                pygame.K_s: settings.DOWN,
                pygame.K_LEFT: settings.LEFT,
                pygame.K_a: settings.LEFT,
                pygame.K_RIGHT: settings.RIGHT,
                pygame.K_d: settings.RIGHT,
            }
            if key in direction_map:
                self.snake.change_direction(direction_map[key])
            elif key == pygame.K_ESCAPE:
                self.state = self.STATE_MENU
        else:  # STATE_GAME_OVER
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.STATE_MENU
            elif key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _render(self):
        """Draw the current state onto the screen."""
        self.screen.fill(settings.COLOR_BACKGROUND)
        if self.state == self.STATE_MENU:
            self._render_menu()
        else:
            self._render_play_field()
            if self.state == self.STATE_GAME_OVER:
                self._render_game_over()
    def _render_menu(self):
        """Draw the difficulty-selection menu."""
        cx = settings.WINDOW_WIDTH // 2
        cy = settings.WINDOW_HEIGHT // 2
        draw_text(self.screen, "CLASSIC SNAKE", settings.FONT_SIZE_TITLE,
                  settings.COLOR_SNAKE_HEAD, center=(cx, cy - 110), bold=True)
        draw_text(self.screen, "Select difficulty (1 / 2 / 3):",
                  settings.FONT_SIZE_MENU, settings.COLOR_TEXT,
                  center=(cx, cy - 30))
        y = cy + 20
        for key, preset in settings.DIFFICULTIES.items():
            draw_text(self.screen,
                      f"[{key}] {preset['name']}  ({preset['speed']} moves/s)",
                      settings.FONT_SIZE_HUD, preset["color"], center=(cx, y))
            y += 34
        draw_text(self.screen, f"Highscore: {self.highscore}",
                  settings.FONT_SIZE_SMALL, settings.COLOR_TEXT_DIM,
                  center=(cx, y + 20))
    def _render_play_field(self):
        """Draw board, grid, food, snake and the HUD score bar."""
        board_rect = pygame.Rect(
            0, settings.HUD_HEIGHT,
            settings.BOARD_WIDTH * settings.CELL_SIZE,
            settings.BOARD_HEIGHT * settings.CELL_SIZE
        )
        pygame.draw.rect(self.screen, settings.COLOR_BOARD, board_rect)
        for gx in range(settings.BOARD_WIDTH + 1):
            x = board_rect.left + gx * settings.CELL_SIZE
            pygame.draw.line(self.screen, settings.COLOR_GRID,
                             (x, board_rect.top), (x, board_rect.bottom))
        for gy in range(settings.BOARD_HEIGHT + 1):
            y = board_rect.top + gy * settings.CELL_SIZE
            pygame.draw.line(self.screen, settings.COLOR_GRID,
                             (board_rect.left, y), (board_rect.right, y))
        if self.food.position is not None:
            fx, fy = self.food.position
            pygame.draw.rect(
                self.screen, settings.COLOR_FOOD,
                (board_rect.left + fx * settings.CELL_SIZE + 2,
                 board_rect.top + fy * settings.CELL_SIZE + 2,
                 settings.CELL_SIZE - 4, settings.CELL_SIZE - 4),
                border_radius=4
            )
        for i, (sx, sy) in enumerate(self.snake.body):
            color = (settings.COLOR_SNAKE_HEAD if i == 0
                     else settings.COLOR_SNAKE_BODY)
            pygame.draw.rect(
                self.screen, color,
                (board_rect.left + sx * settings.CELL_SIZE + 1,
                 board_rect.top + sy * settings.CELL_SIZE + 1,
                 settings.CELL_SIZE - 2, settings.CELL_SIZE - 2),
                border_radius=3
            )
        pygame.draw.rect(self.screen, settings.COLOR_HUD,
                         (0, 0, settings.WINDOW_WIDTH, settings.HUD_HEIGHT))
        preset = settings.DIFFICULTIES[self.difficulty_key]
        draw_text(self.screen, f"Score: {self.score}",
                  settings.FONT_SIZE_HUD, settings.COLOR_TEXT,
                  topleft=(10, 9))
        draw_text(self.screen, f"Highscore: {self.highscore}",
                  settings.FONT_SIZE_HUD, settings.COLOR_TEXT_DIM,
                  center=(settings.WINDOW_WIDTH // 2,
                          settings.HUD_HEIGHT // 2))
        draw_text(self.screen,
                  f"{preset['name']}  {self.speed:.1f} moves/s",
                  settings.FONT_SIZE_HUD, preset["color"],
                  topright=(settings.WINDOW_WIDTH - 10, 9))
    def _render_game_over(self):
        """Draw the semi-transparent game-over overlay."""
        lines = [
            "YOU WIN!" if self.won else "GAME OVER",
            f"Final score: {self.score}",
            f"Highscore: {self.highscore}",
            "ENTER: play again   ESC: quit",
        ]
        draw_overlay(self.screen, lines)