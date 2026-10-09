'''
game.py
Core gameplay for the Classic Snake game: game loop, input handling,
collision rules, scoring, rendering and the pause / game-over screens.
'''
import pygame
import settings
from snake import Snake
from food import Food
from highscore import load_highscore, save_highscore
class Game:
    """Runs one full Snake session at a given difficulty."""
    def __init__(self, screen, difficulty_name):
        self.screen = screen
        self.difficulty_name = difficulty_name
        self.base_speed = settings.DIFFICULTY_LEVELS[difficulty_name]  # moves/sec
        self.clock = pygame.time.Clock()
        self.font_hud = self._get_font(24, bold=True)
        self.font_big = self._get_font(44, bold=True)
        self.font_small = self._get_font(20)
        self.highscore = load_highscore()
        self.reset()
    @staticmethod
    def _get_font(size, bold=False):
        try:
            return pygame.font.SysFont("consolas,menlo,monospace", size, bold=bold)
        except Exception:
            return pygame.font.Font(None, size)
    # ------------------------------------------------------------------
    # Setup / reset
    # ------------------------------------------------------------------
    def reset(self):
        """(Re)initialise all per-session state."""
        start = (settings.GRID_WIDTH // 2, settings.GRID_HEIGHT // 2)
        self.snake = Snake(start, settings.RIGHT, initial_length=3)
        self.food = Food(settings.GRID_WIDTH, settings.GRID_HEIGHT)
        self.food.respawn(self.snake.body)
        self.score = 0
        self.foods_eaten = 0
        self.speed = float(self.base_speed)
        self.move_interval = 1000.0 / self.speed
        self.time_accumulator = 0.0
        self.pending_directions = []
        self.paused = False
        self.game_over = False
        self.won = False
        self.new_highscore = False
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Run one session. Returns 'menu', 'restart' or 'quit'."""
        self._quit = False
        self._restart = False
        self._to_menu = False
        while not (self._quit or self._restart or self._to_menu):
            dt = min(self.clock.tick(settings.FPS_CAP), 100)  # clamp stalls
            self._handle_events()
            if not self.paused and not self.game_over and not self.won:
                self.time_accumulator += dt
                while (self.time_accumulator >= self.move_interval
                       and not self.game_over and not self.won):
                    self.time_accumulator -= self.move_interval
                    self._step()
            self._render()
            pygame.display.flip()
        if self._quit:
            return "quit"
        if self._restart:
            return "restart"
        return "menu"
    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def _handle_events(self):
        """Process keyboard/window events: steering, pause, restart, quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
                return
            if event.type != pygame.KEYDOWN:
                continue
            key = event.key
            ended = self.game_over or self.won
            if key == pygame.K_q:
                self._quit = True
            elif key == pygame.K_ESCAPE:
                if ended:
                    self._to_menu = True
                else:
                    self.paused = not self.paused
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                if ended:
                    self._restart = True
                else:
                    self.paused = not self.paused
            elif key == pygame.K_m and ended:
                self._to_menu = True
            elif key in (pygame.K_UP, pygame.K_w):
                self.pending_directions.append(settings.UP)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.pending_directions.append(settings.DOWN)
            elif key in (pygame.K_LEFT, pygame.K_a):
                self.pending_directions.append(settings.LEFT)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.pending_directions.append(settings.RIGHT)
    # ------------------------------------------------------------------
    # Simulation
    # ------------------------------------------------------------------
    def _step(self):
        """Advance the game by one grid move (collision, food, scoring)."""
        while self.pending_directions:                 # one turn per tick
            d = self.pending_directions.pop(0)
            if self.snake.set_direction(d):
                break
        new_head = self.snake.get_next_head()
        nx, ny = new_head
        if not (0 <= nx < settings.GRID_WIDTH and 0 <= ny < settings.GRID_HEIGHT):
            self._end_game()                           # wall hit
            return
        if self.snake.collides_with_self(new_head):    # self hit
            self._end_game()
            return
        self.snake.move()
        if new_head == self.food.position:             # food eaten
            self.snake.grow(1)
            self.foods_eaten += 1
            self.score += settings.SCORE_PER_FOOD
            if self.foods_eaten % settings.SPEED_UP_EVERY == 0:
                self.speed = min(self.speed + settings.SPEED_UP_STEP,
                                 settings.MAX_SPEED)
                self.move_interval = 1000.0 / self.speed
            if not self.food.respawn(self.snake.body): # board full = win
                self.won = True
                self._register_score()
    def _end_game(self):
        """Enter game-over state and persist the score if it is a record."""
        self.game_over = True
        self._register_score()
    def _register_score(self):
        """Update and save the high score if the current score beats it."""
        if self.score > self.highscore:
            self.highscore = self.score
            self.new_highscore = True
            save_highscore(self.highscore)
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _render(self):
        """Draw playfield, entities, HUD and any overlay screen."""
        self.screen.fill(settings.COLOR_BACKGROUND)
        self._draw_grid()
        self._draw_food()
        self._draw_snake()
        self._draw_border()
        self._draw_hud()
        if self.paused:
            self._draw_overlay("PAUSED", "ESC / SPACE to resume")
        elif self.won:
            self._draw_overlay("YOU WIN!", "Board cleared — ENTER: replay, M: menu")
        elif self.game_over:
            title = "NEW HIGH SCORE!" if self.new_highscore else "GAME OVER"
            self._draw_overlay(title,
                               f"Score: {self.score} — ENTER: replay, M: menu")
    def _cell_rect(self, cell):
        """Pixel rectangle for a grid cell (offset below the HUD bar)."""
        x, y = cell
        return pygame.Rect(x * settings.CELL_SIZE,
                           settings.HUD_HEIGHT + y * settings.CELL_SIZE,
                           settings.CELL_SIZE, settings.CELL_SIZE)
    def _draw_grid(self):
        """Faint grid lines over the playfield."""
        for x in range(settings.GRID_WIDTH + 1):
            px = x * settings.CELL_SIZE
            pygame.draw.line(self.screen, settings.COLOR_GRID_LINE,
                             (px, settings.HUD_HEIGHT),
                             (px, settings.WINDOW_HEIGHT))
        for y in range(settings.GRID_HEIGHT + 1):
            py = settings.HUD_HEIGHT + y * settings.CELL_SIZE
            pygame.draw.line(self.screen, settings.COLOR_GRID_LINE,
                             (0, py), (settings.WINDOW_WIDTH, py))
    def _draw_border(self):
        """Boundary frame around the playfield."""
        pygame.draw.rect(self.screen, settings.COLOR_BORDER,
                         (0, settings.HUD_HEIGHT, settings.WINDOW_WIDTH,
                          settings.WINDOW_HEIGHT - settings.HUD_HEIGHT), 2)
    def _draw_food(self):
        """Food as a red circle centred in its cell."""
        rect = self._cell_rect(self.food.position)
        pygame.draw.circle(self.screen, settings.COLOR_FOOD, rect.center,
                           settings.CELL_SIZE // 2 - 4)
    def _draw_snake(self):
        """Snake body with alternating shades; head brightest."""
        for i, cell in enumerate(self.snake.body):
            color = settings.COLOR_SNAKE_HEAD if i == 0 else (
                settings.COLOR_SNAKE_BODY if i % 2
                else settings.COLOR_SNAKE_BODY_ALT)
            rect = self._cell_rect(cell)
            rect.inflate_ip(-2, -2)
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
    def _draw_hud(self):
        """Top bar: score, difficulty, best, current speed."""
        pygame.draw.rect(self.screen, (24, 24, 24),
                         pygame.Rect(0, 0, settings.WINDOW_WIDTH,
                                     settings.HUD_HEIGHT))
        score_text = self.font_hud.render(f"SCORE: {self.score}", True,
                                          settings.COLOR_TEXT)
        diff_text = self.font_hud.render(
            f"MODE: {self.difficulty_name.upper()}", True,
            settings.COLOR_TEXT_DIM)
        best_text = self.font_hud.render(f"BEST: {self.highscore}", True,
                                         settings.COLOR_TEXT_ACCENT)
        speed_text = self.font_small.render(f"Speed: {self.speed:.0f}/s",
                                            True, settings.COLOR_TEXT_DIM)
        self.screen.blit(score_text, (12, 8))
        self.screen.blit(speed_text, (12, 34))
        self.screen.blit(diff_text,
                         (settings.WINDOW_WIDTH // 2 - diff_text.get_width() // 2, 8))
        self.screen.blit(best_text,
                         (settings.WINDOW_WIDTH - best_text.get_width() - 12, 8))
    def _draw_overlay(self, title, subtitle):
        """Dimmed overlay with centred title + subtitle."""
        overlay = pygame.Surface(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(settings.COLOR_OVERLAY)
        self.screen.blit(overlay, (0, 0))
        t = self.font_big.render(title, True, settings.COLOR_TEXT_ACCENT)
        s = self.font_small.render(subtitle, True, settings.COLOR_TEXT)
        self.screen.blit(t, (settings.WINDOW_WIDTH // 2 - t.get_width() // 2,
                             settings.WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(s, (settings.WINDOW_WIDTH // 2 - s.get_width() // 2,
                             settings.WINDOW_HEIGHT // 2 + 10))