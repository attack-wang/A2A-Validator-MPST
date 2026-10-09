'''
game.py
Defines the Game class: main loop, input handling, piece movement, scoring, and rendering.
'''
import pygame
from constants import (CELL_SIZE, COLS, ROWS, WINDOW_WIDTH, WINDOW_HEIGHT,
                       FPS, BLACK, WHITE, DARK_GRAY, SIDEBAR_BG,
                       BASE_DROP_INTERVAL, MIN_DROP_INTERVAL, DROP_INTERVAL_STEP,
                       LINE_SCORES, LINES_PER_LEVEL,
                       INITIAL_DELAY, REPEAT_DELAY)
from board import Board
from tetromino import Tetromino
class Game:
    """Runs the Tetris game loop, handles input, scoring, and rendering."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 22)
        self.big_font = pygame.font.SysFont("consolas", 36, bold=True)
        self.running = True
        self.reset()
    def reset(self):
        """Reset all game state for a fresh run."""
        self.board = Board()
        self.current = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.drop_interval = self._drop_interval_for_level(self.level)
        self.drop_timer = 0
        self.paused = False
        self.game_over = False
        # Key-repeat state for held movement keys
        self.repeat_timer = 0
        self.first_move_done = False
    @staticmethod
    def _drop_interval_for_level(level):
        """Compute the automatic drop interval (ms) for the given level."""
        return max(MIN_DROP_INTERVAL, BASE_DROP_INTERVAL - (level - 1) * DROP_INTERVAL_STEP)
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_input()
            self.handle_held_keys(dt)
            self.update(dt)
            self.draw()
        pygame.quit()
    def shutdown(self):
        """Stop the main loop and close the game."""
        self.running = False
    # --- Input handling ---
    def handle_input(self):
        """Process keyboard events for movement, rotation, dropping, pause, restart."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.shutdown()
                    continue
                if event.key == pygame.K_r:
                    self.reset()
                    continue
                if self.game_over:
                    continue
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if self.paused:
                    continue
                if event.key == pygame.K_LEFT:
                    self.try_move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.try_move(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.soft_drop()
                elif event.key == pygame.K_UP:
                    self.try_rotate()
                elif event.key == pygame.K_SPACE:
                    self.hard_drop()
    def handle_held_keys(self, dt):
        """Handle continuous movement (left/right/down) with key-repeat delay."""
        if self.game_over or self.paused:
            return
        keys = pygame.key.get_pressed()
        held = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]
        if not held:
            self.repeat_timer = 0
            self.first_move_done = False
            return
        self.repeat_timer += dt
        delay = REPEAT_DELAY if self.first_move_done else INITIAL_DELAY
        if self.repeat_timer >= delay:
            self.repeat_timer = 0
            self.first_move_done = True
            if keys[pygame.K_LEFT]:
                self.try_move(-1, 0)
            elif keys[pygame.K_RIGHT]:
                self.try_move(1, 0)
            elif keys[pygame.K_DOWN]:
                self.soft_drop()
    # --- Piece actions ---
    def try_move(self, dx, dy):
        """Attempt to move the current piece; return True on success."""
        if self.board.is_valid_position(self.current, dx, dy):
            self.current.move(dx, dy)
            return True
        return False
    def try_rotate(self):
        """Attempt to rotate the current piece clockwise (with simple wall kick)."""
        original = self.current.matrix
        self.current.rotate()
        # Try the rotation in place, then nudge left/right/up to resolve collisions
        for dx in (0, -1, 1, -2, 2):
            if self.board.is_valid_position(self.current, dx, 0):
                self.current.move(dx, 0)
                return
        # Rotation impossible: revert
        self.current.matrix = original
    def soft_drop(self):
        """Move the piece one row down; lock it if it cannot move further."""
        if not self.try_move(0, 1):
            self.lock_current()
    def hard_drop(self):
        """Drop the piece instantly to its lowest valid position and lock it."""
        while self.try_move(0, 1):
            pass
        self.lock_current()
    def update(self, dt):
        """Advance automatic gravity and lock the piece when it lands."""
        if self.game_over or self.paused:
            return
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0
            self.soft_drop()
    def lock_current(self):
        """Lock the piece, clear lines, update score/level, and spawn the next piece."""
        self.board.lock_tetromino(self.current)
        cleared = self.board.clear_lines()
        if cleared:
            self.score += LINE_SCORES.get(cleared, 0) * self.level
            self.lines += cleared
            new_level = self.lines // LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.drop_interval = self._drop_interval_for_level(self.level)
        self.spawn_next()
    def spawn_next(self):
        """Promote the next piece to current and check for game over."""
        self.current = self.next_piece
        self.next_piece = Tetromino()
        if self.board.is_game_over(self.current):
            self.game_over = True
    # --- Rendering ---
    def draw_cell(self, surface, col, row, color):
        """Draw a single tetromino cell at board coordinates (col, row)."""
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, DARK_GRAY, rect, 1)
    def draw(self):
        """Render the board, current piece, next-piece preview, and HUD."""
        self.screen.fill(BLACK)
        self.board.draw(self.screen)
        # Draw the current (falling) piece
        for col, row in self.current.get_cells():
            if row >= 0:
                self.draw_cell(self.screen, col, row, self.current.color)
        self.draw_sidebar()
        if self.paused:
            self.draw_center_text("PAUSED")
        elif self.game_over:
            self.draw_center_text("GAME OVER - Press R")
        pygame.display.flip()
    def draw_sidebar(self):
        """Render score, level, lines, and next-piece preview in the sidebar."""
        sidebar_x = COLS * CELL_SIZE
        pygame.draw.rect(self.screen, SIDEBAR_BG,
                         (sidebar_x, 0, WINDOW_WIDTH - sidebar_x, WINDOW_HEIGHT))
        labels = [
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Lines: {self.lines}",
        ]
        for i, text in enumerate(labels):
            label = self.font.render(text, True, WHITE)
            self.screen.blit(label, (sidebar_x + 10, 20 + i * 30))
        next_label = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_label, (sidebar_x + 10, 130))
        # Preview of the next piece
        matrix = self.next_piece.matrix
        preview_x = sidebar_x + 10
        preview_y = 160
        for r, row_vals in enumerate(matrix):
            for c, val in enumerate(row_vals):
                if val:
                    rect = pygame.Rect(preview_x + c * CELL_SIZE,
                                       preview_y + r * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
                    pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
    def draw_center_text(self, text):
        """Render a large message centered over the board."""
        overlay = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        label = self.big_font.render(text, True, WHITE)
        rect = label.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2))
        self.screen.blit(label, rect)