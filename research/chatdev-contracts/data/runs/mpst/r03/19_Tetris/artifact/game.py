'''
game.py
Core game logic for Tetris: the Game class manages the pygame window,
the game loop, player input, piece movement/rotation, gravity timing,
line-clear scoring, level/speed progression, and game-over handling.
'''
import pygame
from constants import (BLACK, WINDOW_WIDTH, WINDOW_HEIGHT,
                       BASE_DROP_INTERVAL, DROP_SPEEDUP_FACTOR,
                       MIN_DROP_INTERVAL, LINES_PER_LEVEL, LINE_SCORES,
                       SOFT_DROP_SCORE, HARD_DROP_SCORE)
from board import Board
from tetromino import Tetromino, PieceBag
import ui
class Game:
    """Main application class: owns the board, current/next pieces,
    score, level, and the main loop."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 42)
        self.huge_font = pygame.font.Font(None, 72)
        self.reset()
    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------
    def reset(self):
        """(Re)initialize all game state; used at start and on restart."""
        self.board = Board()
        self.bag = PieceBag()
        self.current_piece = Tetromino(self.bag.next_type())
        self.next_piece = Tetromino(self.bag.next_type())
        self.score = 0
        self.level = 1
        self.lines = 0
        self.drop_interval = self._drop_interval(self.level)
        self.drop_timer = 0.0
        self.game_over = False
        self.paused = False
    @staticmethod
    def _drop_interval(level):
        """Automatic drop interval (ms) for a level — decreases with each
        level (speeds up) but never below MIN_DROP_INTERVAL."""
        interval = BASE_DROP_INTERVAL * (DROP_SPEEDUP_FACTOR ** (level - 1))
        return max(interval, MIN_DROP_INTERVAL)
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        while True:
            delta_ms = self.clock.tick(60)
            self.handle_events()
            if not self.paused and not self.game_over:
                self.update(delta_ms)
            self.draw()
    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit
        if self.game_over:
            if key == pygame.K_r:
                self.reset()
            return
        if key == pygame.K_p:
            self.paused = not self.paused
            return
        if self.paused:
            return
        if key == pygame.K_LEFT:
            self.try_move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.try_move(1, 0)
        elif key == pygame.K_DOWN:
            if self.try_move(0, 1):
                self.score += SOFT_DROP_SCORE
        elif key == pygame.K_UP:
            self.try_rotate()
        elif key == pygame.K_SPACE:
            self.hard_drop()
        elif key == pygame.K_r:
            self.reset()
    # ------------------------------------------------------------------
    # Piece actions
    # ------------------------------------------------------------------
    def try_move(self, dx, dy):
        """Attempt to move the current piece; returns True on success."""
        if self.board.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True
        return False
    def try_rotate(self):
        """Clockwise rotation with a simple wall-kick fallback."""
        rotated = self.current_piece.rotated_matrix()
        for kick in (0, -1, 1, -2, 2):
            if self.board.is_valid_position(self.current_piece, kick, 0,
                                            matrix=rotated):
                self.current_piece.apply_matrix(rotated)
                self.current_piece.move(kick, 0)
                return True
        return False
    def hard_drop(self):
        """Drop the piece to its landing spot, scoring 2 points per row."""
        rows = 0
        while self.try_move(0, 1):
            rows += 1
        self.score += rows * HARD_DROP_SCORE
        self.lock_current_piece()
    # ------------------------------------------------------------------
    # Update: gravity, locking, line clearing, level progression
    # ------------------------------------------------------------------
    def update(self, delta_ms):
        """Advance the gravity timer; lock the piece when it can't fall."""
        self.drop_timer += delta_ms
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0.0
            if not self.try_move(0, 1):
                self.lock_current_piece()
    def lock_current_piece(self):
        """Lock the piece, clear lines, update score/level, spawn next."""
        self.drop_timer = 0.0
        overflow = self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        if cleared:
            self.score += LINE_SCORES.get(cleared, 0)
            self.lines += cleared
            new_level = 1 + self.lines // LINES_PER_LEVEL
            if new_level > self.level:
                self.level = new_level
                self.drop_interval = self._drop_interval(self.level)
        # Game over if the stack overflowed or the next piece cannot spawn.
        if overflow or not self.board.is_valid_position(self.next_piece):
            self.game_over = True
            return
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(self.bag.next_type())
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(BLACK)
        ui.draw_board(self.screen, self.board)
        ui.draw_ghost_piece(self.screen, self.current_piece, self.board)
        ui.draw_piece(self.screen, self.current_piece)
        ui.draw_sidebar(self.screen, self.font, self.big_font,
                        self.score, self.level, self.lines, self.next_piece)
        if self.paused and not self.game_over:
            ui.draw_overlay(self.screen, self.font, self.huge_font,
                            "PAUSED", "Press P to resume")
        if self.game_over:
            ui.draw_overlay(self.screen, self.font, self.huge_font,
                            "GAME OVER",
                            f"Score: {self.score}  -  Press R to restart")
        pygame.display.flip()