'''
game.py
Defines the Game class containing all gameplay logic and state.
Handles piece spawning (with a one-piece preview), player moves
(shift / rotate / soft drop / hard drop), gravity timing, line-clear
scoring, level progression with increasing fall speed, and the
game-over condition.
'''
import random
from constants import (
    BOARD_WIDTH,
    BOARD_HEIGHT,
    SHAPE_MATRICES,
    SCORE_SINGLE,
    SCORE_DOUBLE,
    SCORE_TRIPLE,
    SCORE_TETRIS,
    SCORE_SOFT_DROP,
    SCORE_HARD_DROP,
    LINES_PER_LEVEL,
    BASE_FALL_DELAY,
    FALL_DELAY_DECREMENT,
    MIN_FALL_DELAY,
)
from tetromino import Tetromino
from board import Board
LINE_SCORES = {
    1: SCORE_SINGLE,
    2: SCORE_DOUBLE,
    3: SCORE_TRIPLE,
    4: SCORE_TETRIS,
}
class Game:
    """Owns the board, the active piece, score, level and gravity."""
    def __init__(self):
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.current_piece = None
        self.next_piece = self._random_piece()
        self.fall_timer = 0.0
        self.fall_delay = self._fall_delay_for_level()
        self.spawn_piece()
    # ------------------------------------------------------------------
    # Piece management
    # ------------------------------------------------------------------
    @staticmethod
    def _random_piece():
        """Return a new Tetromino of a random standard type."""
        return Tetromino(random.choice(list(SHAPE_MATRICES.keys())))
    def _fall_delay_for_level(self):
        """Seconds between automatic gravity drops at the current level."""
        delay = BASE_FALL_DELAY - (self.level - 1) * FALL_DELAY_DECREMENT
        return max(MIN_FALL_DELAY, delay)
    def spawn_piece(self):
        """
        Move the previewed piece into play at the top-centre of the board
        and prepare a new preview piece. If the spawn area is blocked the
        game is over.
        """
        piece = self.next_piece
        piece.x = piece.spawn_x(BOARD_WIDTH)
        piece.y = 0
        if not self.board.is_valid_position(piece, piece.x, piece.y):
            self.current_piece = piece
            self.game_over = True
            return
        self.current_piece = piece
        self.next_piece = self._random_piece()
    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------
    def move_left(self):
        """Shift the active piece one cell left if the move is valid."""
        piece = self.current_piece
        if self.board.is_valid_position(piece, piece.x - 1, piece.y):
            piece.x -= 1
    def move_right(self):
        """Shift the active piece one cell right if the move is valid."""
        piece = self.current_piece
        if self.board.is_valid_position(piece, piece.x + 1, piece.y):
            piece.x += 1
    def rotate(self):
        """
        Rotate the active piece clockwise, trying small horizontal wall-kick
        offsets so rotations near walls/stack still succeed.
        """
        piece = self.current_piece
        rotated = piece.rotated_matrix()
        for offset in piece.rotation_offsets():
            if self.board.is_valid_position(piece, piece.x + offset, piece.y, rotated):
                piece.x += offset
                piece.matrix = rotated
                return
    def soft_drop(self):
        """
        Move the active piece one row down, awarding a point per row.
        Returns True if the piece could move, False if it has landed.
        """
        piece = self.current_piece
        if self.board.is_valid_position(piece, piece.x, piece.y + 1):
            piece.y += 1
            self.score += SCORE_SOFT_DROP
            return True
        return False
    def hard_drop(self):
        """Instantly drop the piece to its landing position and lock it."""
        piece = self.current_piece
        distance = 0
        while self.board.is_valid_position(piece, piece.x, piece.y + 1):
            piece.y += 1
            distance += 1
        self.score += distance * SCORE_HARD_DROP
        self._lock_piece()
    # ------------------------------------------------------------------
    # Locking, clearing and scoring
    # ------------------------------------------------------------------
    def _lock_piece(self):
        """Fix the active piece into the board, clear lines and spawn next."""
        self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        if cleared:
            self.lines += cleared
            self.score += LINE_SCORES.get(cleared, 0) * self.level
            new_level = self.lines // LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.fall_delay = self._fall_delay_for_level()
        self.spawn_piece()
    # ------------------------------------------------------------------
    # Frame update
    # ------------------------------------------------------------------
    def update(self, dt):
        """Advance gravity by `dt` seconds; lock the piece when it lands."""
        if self.game_over or self.current_piece is None:
            return
        self.fall_timer += dt
        if self.fall_timer < self.fall_delay:
            return
        self.fall_timer = 0.0
        piece = self.current_piece
        if self.board.is_valid_position(piece, piece.x, piece.y + 1):
            piece.y += 1
        else:
            self._lock_piece()
    def restart(self):
        """Reset all state so a fresh game can start."""
        self.board.reset()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.fall_timer = 0.0
        self.fall_delay = self._fall_delay_for_level()
        self.next_piece = self._random_piece()
        self.spawn_piece()