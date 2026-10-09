'''
game.py
Defines the Game class: pygame main loop, input handling (move, rotate,
soft/hard drop), gravity with level-based speed, scoring, line clearing,
ghost piece, next-piece preview, HUD rendering, game-over overlay and
high-score persistence.
'''
import pygame
from constants import (BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, FPS,
                       SIDEBAR_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT,
                       COLOR_BG, COLOR_GRID, COLOR_BORDER, COLOR_TEXT,
                       COLOR_GHOST, LINE_SCORES, SOFT_DROP_POINTS,
                       HARD_DROP_POINTS, LINES_PER_LEVEL,
                       BASE_DROP_INTERVAL, MIN_DROP_INTERVAL,
                       SPEEDUP_FACTOR, HIGHSCORE_FILE)
from tetromino import Tetromino, BagRandomizer
from board import Board
MOVE_REPEAT_DELAY = 0.12  # seconds between repeated held-key moves
class Game:
    """Runs the Tetris game: state, input, gravity, scoring and rendering."""
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.small_font = pygame.font.SysFont("consolas", 14)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)
        self.board = Board()
        self.randomizer = BagRandomizer()
        self.high_score = self._load_high_score()
        self.reset()
    # ------------------------------------------------------------------ #
    # State management
    # ------------------------------------------------------------------ #
    def reset(self):
        """(Re)initialize a fresh game state."""
        self.board.reset()
        self.randomizer = BagRandomizer()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.drop_interval = self._drop_interval_for_level()
        self.drop_timer = 0.0
        self._move_cooldown = 0.0
        self.game_over = False
        self.next_key = self.randomizer.next_shape()
        self._spawn_tetromino()
    def _drop_interval_for_level(self):
        """Return the gravity interval (seconds) for the current level."""
        interval = BASE_DROP_INTERVAL * (SPEEDUP_FACTOR ** (self.level - 1))
        return max(interval, MIN_DROP_INTERVAL)
    def _spawn_tetromino(self):
        """Create the next falling piece; trigger game over if it cannot fit."""
        self.current_tetromino = Tetromino(self.next_key)
        self.next_key = self.randomizer.next_shape()
        if not self.board.is_valid_position(self.current_tetromino):
            self.current_tetromino = None
            self._trigger_game_over()
    # ------------------------------------------------------------------ #
    # High score persistence
    # ------------------------------------------------------------------ #
    def _load_high_score(self):
        """Read the persisted high score; return 0 if unavailable."""
        try:
            with open(HIGHSCORE_FILE) as f:
                return int(f.read().strip() or 0)
        except (IOError, ValueError):
            return 0
    def _save_high_score(self):
        """Persist the current high score to disk."""
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(self.high_score))
        except IOError:
            pass
    # ------------------------------------------------------------------ #
    # Scoring
    # ------------------------------------------------------------------ #
    def update_score(self, cleared_lines):
        """Add line-clear points, update lines/level and the high score."""
        if cleared_lines:
            self.score += LINE_SCORES.get(cleared_lines, 0) * self.level
            self.lines += cleared_lines
            new_level = self.lines // LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.drop_interval = self._drop_interval_for_level()
        if self.score > self.high_score:
            self.high_score = self.score
    def add_drop_points(self, cells, hard):
        """Award soft/hard drop points for manually dropped cells."""
        if cells > 0:
            self.score += cells * (HARD_DROP_POINTS if hard else SOFT_DROP_POINTS)
            if self.score > self.high_score:
                self.high_score = self.score
    def _trigger_game_over(self):
        """Flag game over and persist the high score."""
        self.game_over = True
        if self.score >= self.high_score:
            self._save_high_score()
    # ------------------------------------------------------------------ #
    # Piece movement
    # ------------------------------------------------------------------ #
    def try_move(self, dx, dy):
        """Attempt to shift the piece; return True on success."""
        if self.board.is_valid_position(self.current_tetromino, dx, dy):
            self.current_tetromino.move(dx, dy)
            return True
        return False
    def try_rotate(self):
        """Rotate the piece clockwise with simple wall/floor kicks."""
        piece = self.current_tetromino
        rotated = piece.rotated_matrix()
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)):
            if self.board.is_valid_position(piece, dx, dy, matrix=rotated):
                piece.matrix = rotated
                piece.move(dx, dy)
                return True
        return False
    def soft_drop(self):
        """Move the piece one row down; lock it if it cannot move."""
        if self.try_move(0, 1):
            self.add_drop_points(1, hard=False)
        else:
            self.lock_current()
    def hard_drop(self):
        """Drop the piece instantly to the lowest valid position and lock it."""
        piece = self.current_tetromino
        cells = 0
        while self.board.is_valid_position(piece, 0, 1):
            piece.move(0, 1)
            cells += 1
        self.add_drop_points(cells, hard=True)
        self.lock_current()
    def lock_current(self):
        """Lock the piece, clear lines, update score and spawn the next piece."""
        self.drop_timer = 0.0
        if self.board.lock_tetromino(self.current_tetromino):
            cleared = self.board.clear_lines()
            self.update_score(cleared)
            self._spawn_tetromino()
        else:
            self._trigger_game_over()
    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def run(self):
        """Run the pygame event/render loop until the user quits."""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_keydown(event)
            self._update(dt)
            self._draw()
            pygame.display.flip()
        pygame.quit()
    def _update(self, dt):
        """Advance gravity and handle held-key movement for this frame."""
        if self.game_over or self.current_tetromino is None:
            return
        # Held-key horizontal / soft-drop movement with a small cooldown
        self._move_cooldown -= dt
        if self._move_cooldown <= 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.try_move(-1, 0)
                self._move_cooldown = MOVE_REPEAT_DELAY
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.try_move(1, 0)
                self._move_cooldown = MOVE_REPEAT_DELAY
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.soft_drop()
                self._move_cooldown = MOVE_REPEAT_DELAY
        if self.game_over or self.current_tetromino is None:
            return  # a soft drop may have locked the piece and ended the game
        # Gravity
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0.0
            if not self.try_move(0, 1):
                self.lock_current()
    def _handle_keydown(self, event):
        """Translate key presses into game actions (rotate, hard drop, restart)."""
        if self.game_over:
            if event.key == pygame.K_r:
                self.reset()
            return
        if event.key in (pygame.K_UP, pygame.K_w):
            self.try_rotate()
        elif event.key == pygame.K_SPACE:
            self.hard_drop()
        elif event.key == pygame.K_r:
            self.reset()
    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def _ghost_cells(self):
        """Return the board cells where the current piece would land."""
        piece = self.current_tetromino
        dy = 0
        while self.board.is_valid_position(piece, 0, dy + 1):
            dy += 1
        return piece.get_cells(piece.matrix, piece.x, piece.y + dy)
    def _draw_cell_px(self, px, py, color):
        """Draw one cell at pixel position (px, py) with a slight border."""
        rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.window, color, rect)
        pygame.draw.rect(self.window, COLOR_BORDER, rect, 1)
    def _draw_cell(self, col, row, color):
        """Draw one board cell at grid coordinates (col, row)."""
        self._draw_cell_px(col * CELL_SIZE, row * CELL_SIZE, color)
    def _draw(self):
        """Render board, locked cells, current piece, ghost, HUD and overlays."""
        self.window.fill(COLOR_BG)
        # Grid lines
        for col in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.window, COLOR_GRID,
                             (col * CELL_SIZE, 0),
                             (col * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE))
        for row in range(BOARD_HEIGHT + 1):
            pygame.draw.line(self.window, COLOR_GRID,
                             (0, row * CELL_SIZE),
                             (BOARD_WIDTH * CELL_SIZE, row * CELL_SIZE))
        # Locked cells
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                color = self.board.grid[row][col]
                if color is not None:
                    self._draw_cell(col, row, color)
        if self.current_tetromino is not None:
            # Ghost (landing preview) piece
            for col, row in self._ghost_cells():
                if row >= 0:
                    rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.window, COLOR_GHOST, rect, 1)
            # Current falling piece
            for col, row in self.current_tetromino.get_cells():
                if row >= 0:
                    self._draw_cell(col, row, self.current_tetromino.color)
        # Playfield border
        pygame.draw.rect(self.window, COLOR_BORDER,
                         (0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE), 2)
        self._draw_sidebar()
        if self.game_over:
            self._draw_game_over()
    def _draw_sidebar(self):
        """Render score, level, lines, high score, next-piece preview and help."""
        sidebar_x = BOARD_WIDTH * CELL_SIZE + 10
        texts = [
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Lines: {self.lines}",
            f"High:  {self.high_score}",
        ]
        for i, text in enumerate(texts):
            label = self.font.render(text, True, COLOR_TEXT)
            self.window.blit(label, (sidebar_x, 20 + i * 30))
        next_label = self.font.render("Next:", True, COLOR_TEXT)
        self.window.blit(next_label, (sidebar_x, 150))
        next_tetromino = Tetromino(self.next_key)
        preview_x = sidebar_x + (SIDEBAR_WIDTH - 20 - next_tetromino.width * CELL_SIZE) // 2
        for col, row in next_tetromino.get_cells(offset_x=0, offset_y=0):
            self._draw_cell_px(preview_x + col * CELL_SIZE, 180 + row * CELL_SIZE,
                               next_tetromino.color)
        hints = [
            "Left/Right: move",
            "Down: soft drop",
            "Up: rotate",
            "Space: hard drop",
            "R: restart",
        ]
        for i, hint in enumerate(hints):
            label = self.small_font.render(hint, True, COLOR_TEXT)
            self.window.blit(label, (sidebar_x, WINDOW_HEIGHT - 110 + i * 20))
    def _draw_game_over(self):
        """Show the game-over overlay with the final score and restart hint."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.window.blit(overlay, (0, 0))
        title = self.big_font.render("GAME OVER", True, COLOR_TEXT)
        score_text = self.font.render(f"Final score: {self.score}", True, COLOR_TEXT)
        hint = self.font.render("Press R to restart", True, COLOR_TEXT)
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        self.window.blit(title, title.get_rect(center=(center_x, center_y - 30)))
        self.window.blit(score_text, score_text.get_rect(center=(center_x, center_y + 10)))
        self.window.blit(hint, hint.get_rect(center=(center_x, center_y + 40)))