'''
game.py
Defines the Game class holding all gameplay state and rules: spawning
pieces, applying player moves/rotations, gravity ticks, locking pieces,
clearing lines, scoring, level progression and game-over detection.
'''
import random
from constants import (COLS, ROWS, LINE_SCORES, SOFT_DROP_SCORE,
                       HARD_DROP_SCORE, LINES_PER_LEVEL, get_drop_interval)
from tetromino import Tetromino
from board import Board
class Game:
    """Core Tetris gameplay logic, independent of rendering."""
    def __init__(self):
        self.board = Board(COLS, ROWS)
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.current_piece = None
        self.next_piece = Tetromino()
        self.drop_timer_ms = 0
        self.spawn_piece()
    def spawn_piece(self):
        """Bring the next piece into play; end the game if it cannot fit."""
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        # Center the piece horizontally at the top
        spawn_x = (self.board.cols - len(self.current_piece.shape[0])) // 2
        self.current_piece.set_position(spawn_x, 0)
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    def move_piece(self, dx, dy):
        """Try to shift the piece; return True on success."""
        if self.game_over:
            return False
        if self.board.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True
        return False
    def rotate_piece(self):
        """Try to rotate the piece clockwise (with simple wall kicks)."""
        if self.game_over:
            return False
        rotated = self.current_piece.rotated_shape()
        # Try rotation in place, then small kicks left/right/up
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0)):
            if self.board.is_valid_position(self.current_piece, dx, dy, shape=rotated):
                self.current_piece.shape = rotated
                self.current_piece.move(dx, dy)
                return True
        return False
    def soft_drop(self):
        """Move the piece one cell down manually; award a point on success."""
        if self.move_piece(0, 1):
            self.score += SOFT_DROP_SCORE
            return True
        return False
    def hard_drop(self):
        """Drop the piece instantly to its lowest position; award points."""
        distance = 0
        while self.board.is_valid_position(self.current_piece, 0, 1):
            self.current_piece.move(0, 1)
            distance += 1
        self.score += distance * HARD_DROP_SCORE
        self.lock_current_piece()
    def update(self, elapsed_ms):
        """Advance gravity by elapsed_ms; lock the piece when it lands."""
        if self.game_over:
            return
        self.drop_timer_ms += elapsed_ms
        interval = get_drop_interval(self.level)
        while self.drop_timer_ms >= interval:
            self.drop_timer_ms -= interval
            if not self.move_piece(0, 1):
                self.lock_current_piece()
                break
    def lock_current_piece(self):
        """Freeze the piece into the grid, clear lines, update score/level."""
        top_out = self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        if cleared:
            self.score += LINE_SCORES.get(cleared, 800) * self.level
            self.lines += cleared
            self.level = self.lines // LINES_PER_LEVEL + 1
        self.drop_timer_ms = 0
        if top_out:
            self.game_over = True
        else:
            self.spawn_piece()