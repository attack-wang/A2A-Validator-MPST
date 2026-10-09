'''
game.py
Core engine for the Classic Snake game.
Manages game states (difficulty menu, playing, paused, game over),
keyboard input, the fixed-timestep game loop, collision rules,
score tracking and all rendering.
'''
import os
import pygame
import settings
from snake import Snake
from food import Food
HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")
class Game:
    """Top-level application: owns the window, states and the main loop."""
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Classic Snake - ChatDev")
        self.clock = pygame.time.Clock()
        self.font_hud = pygame.font.SysFont("consolas", settings.FONT_SIZE_HUD, bold=True)
        self.font_title = pygame.font.SysFont("consolas", settings.FONT_SIZE_TITLE, bold=True)
        self.font_menu = pygame.font.SysFont("consolas", settings.FONT_SIZE_MENU, bold=True)
        self.font_message = pygame.font.SysFont("consolas", settings.FONT_SIZE_MESSAGE)
        self.font_small = pygame.font.SysFont("consolas", settings.FONT_SIZE_SMALL)
        self.state = self.STATE_MENU
        self.difficulty_name = "Medium"
        self.high_score = self._load_high_score()
        self.new_high_score = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.won = False
        self.move_accumulator = 0.0
        self.running = False
        self.menu_options = list(settings.DIFFICULTY_ORDER)
        if self.difficulty_name in self.menu_options:
            self.menu_index = self.menu_options.index(self.difficulty_name)
        else:
            self.menu_index = 0
            self.difficulty_name = self.menu_options[self.menu_index]
    # ------------------------------------------------------------------ #
    # High score persistence
    # ------------------------------------------------------------------ #
    def _load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as fh:
                return int(fh.read().strip() or 0)
        except (FileNotFoundError, ValueError, OSError):
            return 0
    def _save_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as fh:
                fh.write(str(self.high_score))
        except OSError:
            pass
    def _commit_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_high_score = True
            self._save_high_score()
        else:
            self.new_high_score = False
    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def run(self):
        self.running = True
        while self.running:
            delta_ms = self.clock.tick(settings.FPS)
            self._handle_events()
            self.update(delta_ms)
            self._render()
        pygame.quit()
    # ------------------------------------------------------------------ #
    # Input handling
    # ------------------------------------------------------------------ #
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
    def _handle_keydown(self, key):
        if self.state == self.STATE_MENU:
            self._menu_keydown(key)
        elif self.state == self.STATE_PLAYING:
            self._playing_keydown(key)
        elif self.state == self.STATE_PAUSED:
            self._paused_keydown(key)
        elif self.state == self.STATE_GAME_OVER:
            self._game_over_keydown(key)
    def _menu_keydown(self, key):
        if key in (pygame.K_UP, pygame.K_w):
            self.menu_index = (self.menu_index - 1) % len(self.menu_options)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.menu_index = (self.menu_index + 1) % len(self.menu_options)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.difficulty_name = self.menu_options[self.menu_index]
            self._start_game()
        elif key == pygame.K_ESCAPE:
            self.running = False
    def _playing_keydown(self, key):
        direction_map = {
            pygame.K_UP: settings.DIR_UP,
            pygame.K_w: settings.DIR_UP,
            pygame.K_DOWN: settings.DIR_DOWN,
            pygame.K_s: settings.DIR_DOWN,
            pygame.K_LEFT: settings.DIR_LEFT,
            pygame.K_a: settings.DIR_LEFT,
            pygame.K_RIGHT: settings.DIR_RIGHT,
            pygame.K_d: settings.DIR_RIGHT,
        }
        if key in direction_map:
            self.snake.queue_direction(direction_map[key])
        elif key in (pygame.K_p, pygame.K_ESCAPE):
            self.state = self.STATE_PAUSED
    def _paused_keydown(self, key):
        if key in (pygame.K_p, pygame.K_RETURN, pygame.K_SPACE):
            self.state = self.STATE_PLAYING
        elif key == pygame.K_ESCAPE:
            self.state = self.STATE_MENU
    def _game_over_keydown(self, key):
        if key in (pygame.K_RETURN, pygame.K_SPACE):
            self._start_game()
        elif key == pygame.K_ESCAPE:
            self.state = self.STATE_MENU
    # ------------------------------------------------------------------ #
    # Game lifecycle
    # ------------------------------------------------------------------ #
    def _start_game(self):
        self.snake.reset()
        self.food.randomize(self.snake.get_body())
        self.score = 0
        self.won = False
        self.new_high_score = False
        self.move_accumulator = 0.0
        self.state = self.STATE_PLAYING
    def _game_over(self):
        self._commit_high_score()
        self.state = self.STATE_GAME_OVER
    # ------------------------------------------------------------------ #
    # Update logic (fixed timestep)
    # ------------------------------------------------------------------ #
    def update(self, delta_ms):
        if self.state != self.STATE_PLAYING:
            return
        self.move_accumulator += delta_ms / 1000.0
        speed = settings.DIFFICULTIES[self.difficulty_name]["speed"]
        move_interval = 1.0 / speed
        # Guard against huge delta (e.g. window drag) to avoid spiral
        if self.move_accumulator > 0.5:
            self.move_accumulator = 0.5
        while self.move_accumulator >= move_interval:
            self.move_accumulator -= move_interval
            self._tick()
            if self.state != self.STATE_PLAYING:
                break
    def _tick(self):
        self.snake.apply_queued_turn()
        new_head = self.snake.compute_next_head()
        nx, ny = new_head
        # Boundary collision
        if nx < 0 or nx >= settings.GRID_WIDTH or ny < 0 or ny >= settings.GRID_HEIGHT:
            self._game_over()
            return
        growing = (new_head == self.food.get_position())
        # Self collision (tail cell is safe when it will move away this tick)
        if self.snake.collides_with_point(new_head, ignore_tail=not growing):
            self._game_over()
            return
        self.snake.advance(grow=growing)
        if growing:
            self.score += 1
            self.food.randomize(self.snake.get_body())
            if self.food.get_position() is None:
                # Board completely filled -> win
                self._commit_high_score()
                self.won = True
                self.state = self.STATE_GAME_OVER
    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def _render(self):
        self.screen.fill(settings.COLOR_BACKGROUND)
        if self.state == self.STATE_MENU:
            self._draw_menu()
        elif self.state == self.STATE_PLAYING:
            self._draw_board()
            self._draw_food()
            self._draw_snake()
            self._draw_hud()
        elif self.state == self.STATE_PAUSED:
            self._draw_board()
            self._draw_food()
            self._draw_snake()
            self._draw_hud()
            self._draw_overlay("PAUSED", [
                "Press P or ENTER to resume",
                "Press ESC for menu",
            ])
        elif self.state == self.STATE_GAME_OVER:
            self._draw_board()
            self._draw_food()
            self._draw_snake()
            self._draw_hud()
            self._draw_game_over()
        pygame.display.flip()
    def _draw_hud(self):
        hud_rect = pygame.Rect(0, 0, settings.WINDOW_WIDTH, settings.HUD_HEIGHT)
        pygame.draw.rect(self.screen, settings.COLOR_HUD, hud_rect)
        accent = settings.DIFFICULTIES[self.difficulty_name]["color"]
        pygame.draw.line(
            self.screen, accent,
            (0, settings.HUD_HEIGHT - 2),
            (settings.WINDOW_WIDTH, settings.HUD_HEIGHT - 2),
            2,
        )
        score_text = self.font_hud.render(f"SCORE: {self.score}", True, settings.COLOR_HUD_TEXT)
        high_text = self.font_hud.render(f"HIGH: {self.high_score}", True, settings.COLOR_HUD_TEXT)
        diff_text = self.font_hud.render(self.difficulty_name.upper(), True, accent)
        self.screen.blit(score_text, (16, 14))
        self.screen.blit(diff_text, (settings.WINDOW_WIDTH // 2 - diff_text.get_width() // 2, 14))
        self.screen.blit(high_text, (settings.WINDOW_WIDTH - high_text.get_width() - 16, 14))
    def _draw_board(self):
        board_top = settings.HUD_HEIGHT
        for y in range(settings.GRID_HEIGHT):
            for x in range(settings.GRID_WIDTH):
                color = settings.COLOR_GRID_A if (x + y) % 2 == 0 else settings.COLOR_GRID_B
                rect = pygame.Rect(
                    x * settings.GRID_SIZE,
                    board_top + y * settings.GRID_SIZE,
                    settings.GRID_SIZE,
                    settings.GRID_SIZE,
                )
                pygame.draw.rect(self.screen, color, rect)
    def _cell_rect(self, cell):
        x, y = cell
        return pygame.Rect(
            x * settings.GRID_SIZE,
            settings.HUD_HEIGHT + y * settings.GRID_SIZE,
            settings.GRID_SIZE,
            settings.GRID_SIZE,
        )
    def _draw_snake(self):
        body = self.snake.get_body()
        for i, cell in enumerate(body):
            rect = self._cell_rect(cell)
            color = settings.COLOR_SNAKE_HEAD if i == 0 else settings.COLOR_SNAKE_BODY
            pygame.draw.rect(self.screen, color, rect.inflate(-4, -4), border_radius=6)
            pygame.draw.rect(self.screen, settings.COLOR_SNAKE_BORDER, rect.inflate(-4, -4), width=2, border_radius=6)
    def _draw_food(self):
        pos = self.food.get_position()
        if pos is None:
            return
        rect = self._cell_rect(pos)
        pygame.draw.circle(self.screen, settings.COLOR_FOOD, rect.center, settings.GRID_SIZE // 2 - 4)
        highlight_center = (rect.centerx - 3, rect.centery - 3)
        pygame.draw.circle(self.screen, settings.COLOR_FOOD_HIGHLIGHT, highlight_center, 3)
    def _draw_center_text(self, font, text, color, y_offset):
        surface = font.render(text, True, color)
        rect = surface.get_rect(
            center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + y_offset)
        )
        self.screen.blit(surface, rect)
    def _draw_menu(self):
        self._draw_center_text(self.font_title, "CLASSIC SNAKE", settings.COLOR_TITLE, -160)
        self._draw_center_text(self.font_message, "Select difficulty (UP/DOWN, ENTER to start)", settings.COLOR_TEXT, -100)
        for i, option in enumerate(self.menu_options):
            color = settings.COLOR_MENU_HIGHLIGHT if i == self.menu_index else settings.COLOR_MENU_NORMAL
            prefix = "> " if i == self.menu_index else "  "
            text = f"{prefix}{option}"
            self._draw_center_text(self.font_menu, text, color, -30 + i * 44)
        self._draw_center_text(self.font_small, f"High score: {self.high_score}", settings.COLOR_TEXT, 90)
        self._draw_center_text(self.font_small, "ESC to quit", settings.COLOR_TEXT, 130)
    def _draw_overlay(self, title, lines):
        overlay = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        self._draw_center_text(self.font_title, title, settings.COLOR_TITLE, -120)
        y_offset = -40
        for line in lines:
            if line:
                self._draw_center_text(self.font_message, line, settings.COLOR_TEXT, y_offset)
            y_offset += 34
    def _draw_game_over(self):
        if self.won:
            title = "YOU WIN!"
            lines = [
                "You filled the entire board!",
                f"Final score: {self.score}",
                f"High score: {self.high_score}",
                "",
                "Press ENTER or SPACE to play again",
                "Press ESC for menu",
            ]
        else:
            title = "GAME OVER"
            lines = [
                f"Final score: {self.score}",
                f"High score: {self.high_score}",
            ]
            if self.new_high_score:
                lines.insert(2, "*** NEW HIGH SCORE! ***")
            lines += [
                "",
                "Press ENTER or SPACE to play again",
                "Press ESC for menu",
            ]
        self._draw_overlay(title, lines)