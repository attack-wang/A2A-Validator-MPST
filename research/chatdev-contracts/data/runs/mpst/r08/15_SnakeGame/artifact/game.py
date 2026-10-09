'''
game.py
Core Snake game logic: event handling, state updates (movement, food
consumption, collisions), rendering of board/snake/food/HUD, pause and
game-over flows.
'''
import pygame
import settings as cfg
from snake import Snake, DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT
from food import Food
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
class Game:
    '''Runs one full session of the Snake game at a given difficulty.'''
    def __init__(self, screen, difficulty, high_score=0):
        self.screen = screen
        self.difficulty = difficulty
        self.moves_per_second = cfg.DIFFICULTY_SETTINGS[difficulty]
        self.score_multiplier = cfg.SCORE_MULTIPLIERS.get(difficulty, 1)
        self.font_header = pygame.font.SysFont(None, cfg.FONT_SIZE_HEADER, bold=True)
        self.font_message = pygame.font.SysFont(None, cfg.FONT_SIZE_MESSAGE)
        self.font_big = pygame.font.SysFont(None, 64, bold=True)
        self.clock = pygame.time.Clock()
        self.high_score = high_score
        self.best_score = high_score  # persists across in-session restarts
        self.reset()
    def reset(self):
        '''(Re)initialize all per-session state (best_score is preserved).'''
        self.snake = Snake(cfg.GRID_WIDTH // 2, cfg.GRID_HEIGHT // 2, initial_length=3)
        self.food = Food(cfg.GRID_WIDTH, cfg.GRID_HEIGHT, self.snake.body)
        self.score = 0
        self.state = STATE_PLAYING
        self.won = False  # FIX: initialize win flag so overlays never crash
        self.move_timer = 0.0
        self.move_interval = 1.0 / self.moves_per_second
    def handle_events(self):
        '''Process input. Returns "quit", "menu", or None to continue.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type != pygame.KEYDOWN:
                continue
            key = event.key
            if self.state == STATE_PLAYING:
                if key in (pygame.K_UP, pygame.K_w):
                    self.snake.set_direction(DIR_UP)
                elif key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.set_direction(DIR_DOWN)
                elif key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.set_direction(DIR_LEFT)
                elif key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.set_direction(DIR_RIGHT)
                elif key in (pygame.K_p, pygame.K_SPACE):
                    self.state = STATE_PAUSED
                elif key == pygame.K_ESCAPE:
                    return "menu"
            elif self.state == STATE_PAUSED:
                if key in (pygame.K_p, pygame.K_SPACE):
                    self.state = STATE_PLAYING
                elif key == pygame.K_ESCAPE:
                    return "menu"
            elif self.state == STATE_GAME_OVER:
                if key == pygame.K_r:
                    self.reset()
                elif key in (pygame.K_m, pygame.K_ESCAPE):
                    return "menu"
        return None
    def update(self, dt):
        '''Advance game logic by `dt` seconds (time-based, frame-rate independent).'''
        if self.state != STATE_PLAYING:
            return
        self.move_timer += dt
        while self.move_timer >= self.move_interval:
            self.move_timer -= self.move_interval
            self.step()
            if self.state != STATE_PLAYING:  # stop stepping after death/win
                self.move_timer = 0.0
                break
    def step(self):
        '''Perform a single grid move: move snake, check collisions, eat food.'''
        self.snake.move()
        if self.snake.hits_boundary(cfg.GRID_WIDTH, cfg.GRID_HEIGHT) or self.snake.hits_self():
            self.state = STATE_GAME_OVER
            self.won = False
            return
        if self.food.exists and self.snake.body[0] == self.food.position:
            self.score += cfg.SCORE_PER_FOOD * self.score_multiplier
            self.best_score = max(self.best_score, self.score)
            self.snake.grow(1)
            self.food.randomize_position(self.snake.body)
            if not self.food.exists:  # board completely filled -> victory
                self.state = STATE_GAME_OVER
                self.won = True
    def render(self):
        '''Draw one full frame: header, clipped board, food, snake, overlays.'''
        self.screen.fill(cfg.COLOR_BACKGROUND)
        self._render_header()
        board_rect = pygame.Rect(
            0, cfg.BOARD_TOP,
            cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT - cfg.BOARD_TOP,
        )
        self.screen.set_clip(board_rect)  # clip so nothing leaks into the header
        self._render_board()
        self._render_food()
        self._render_snake()
        self.screen.set_clip(None)
        if self.state == STATE_PAUSED:
            self._render_overlay("PAUSED", "Press P or SPACE to resume | ESC for menu")
        elif self.state == STATE_GAME_OVER:
            title = "YOU WIN!" if self.won else "GAME OVER"
            self._render_overlay(
                title,
                f"Final score: {self.score}   |   R: restart   M: menu",
            )
        pygame.display.flip()
    def _render_header(self):
        '''Draw the top HUD bar with current score, best score and difficulty.'''
        header_rect = pygame.Rect(0, 0, cfg.SCREEN_WIDTH, cfg.HEADER_HEIGHT)
        pygame.draw.rect(self.screen, (28, 28, 34), header_rect)
        score_text = self.font_header.render(
            f"Score: {self.score}   Best: {self.best_score}", True, cfg.COLOR_TEXT
        )
        self.screen.blit(score_text, (12, 10))
        diff_text = self.font_header.render(
            f"Difficulty: {self.difficulty}", True, cfg.COLOR_TEXT_DIM
        )
        diff_rect = diff_text.get_rect(right=cfg.SCREEN_WIDTH - 12, top=10)
        self.screen.blit(diff_text, diff_rect)
    def _render_board(self):
        '''Draw playfield background, subtle grid lines, and border.'''
        board_rect = pygame.Rect(
            0, cfg.BOARD_TOP,
            cfg.CELL_SIZE * cfg.GRID_WIDTH,
            cfg.CELL_SIZE * cfg.GRID_HEIGHT,
        )
        pygame.draw.rect(self.screen, cfg.COLOR_BACKGROUND, board_rect)
        board_bottom = cfg.BOARD_TOP + cfg.CELL_SIZE * cfg.GRID_HEIGHT
        board_right = cfg.CELL_SIZE * cfg.GRID_WIDTH
        for x in range(cfg.GRID_WIDTH + 1):  # vertical lines
            px = x * cfg.CELL_SIZE
            pygame.draw.line(
                self.screen, cfg.COLOR_GRID_LINE,
                (px, cfg.BOARD_TOP), (px, board_bottom),
            )
        for y in range(cfg.GRID_HEIGHT + 1):  # horizontal lines
            py = cfg.BOARD_TOP + y * cfg.CELL_SIZE
            pygame.draw.line(
                self.screen, cfg.COLOR_GRID_LINE,
                (0, py), (board_right, py),
            )
        pygame.draw.rect(self.screen, cfg.COLOR_BOARD_BORDER, board_rect, 2)
    def _cell_rect(self, cell):
        '''Convert a grid cell (x, y) to a pixel Rect on the playfield.'''
        x, y = cell
        return pygame.Rect(
            x * cfg.CELL_SIZE,
            cfg.BOARD_TOP + y * cfg.CELL_SIZE,
            cfg.CELL_SIZE,
            cfg.CELL_SIZE,
        )
    def _render_food(self):
        '''Draw the food as a red "apple" with a small stem.'''
        if not self.food.exists:
            return
        rect = self._cell_rect(self.food.position)
        center = rect.center
        pygame.draw.circle(
            self.screen, cfg.COLOR_FOOD, center, cfg.CELL_SIZE // 2 - 4
        )
        pygame.draw.line(
            self.screen, (120, 70, 30),
            (center[0], rect.top + 3), (center[0], rect.top + 8), 3,
        )
    def _render_snake(self):
        '''Draw every snake segment; head is brighter with rounded corners.'''
        for i, cell in enumerate(self.snake.body):
            rect = self._cell_rect(cell)
            rect.inflate_ip(-2, -2)  # small gap between segments
            color = cfg.COLOR_SNAKE_HEAD if i == 0 else cfg.COLOR_SNAKE_BODY
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
    def _render_overlay(self, title, message):
        '''Draw a dimming overlay with a centered title and message.'''
        overlay = pygame.Surface(
            (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill(
            (cfg.COLOR_OVERLAY[0], cfg.COLOR_OVERLAY[1], cfg.COLOR_OVERLAY[2], 190)
        )
        self.screen.blit(overlay, (0, 0))
        title_text = self.font_big.render(title, True, cfg.COLOR_TEXT)
        title_rect = title_text.get_rect(
            center=(cfg.SCREEN_WIDTH // 2, cfg.SCREEN_HEIGHT // 2 - 40)
        )
        self.screen.blit(title_text, title_rect)
        msg_text = self.font_message.render(message, True, cfg.COLOR_TEXT_DIM)
        msg_rect = msg_text.get_rect(
            center=(cfg.SCREEN_WIDTH // 2, cfg.SCREEN_HEIGHT // 2 + 30)
        )
        self.screen.blit(msg_text, msg_rect)
    def run(self):
        '''Run the game session loop. Returns "menu" or "quit".'''
        while True:
            dt = self.clock.tick(cfg.RENDER_FPS) / 1000.0
            action = self.handle_events()
            if action is not None:
                return action
            self.update(dt)
            self.render()