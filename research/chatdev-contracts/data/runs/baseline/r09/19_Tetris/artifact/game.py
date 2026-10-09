'''
game.py
Defines the Game class: the state machine and rules engine of Tetris.
Responsibilities:
  * spawn pieces (with a one-piece "next" preview and 7-bag randomizer),
  * apply player moves (shift, rotate with wall kicks, soft/hard drop),
  * advance gravity on a timer that speeds up with the level,
  * lock pieces, clear lines, award score, raise the level,
  * detect game over and support restart / pause.
'''
import random
from settings import (SHAPES, LINE_SCORES, SOFT_DROP_SCORE, HARD_DROP_SCORE,
                      LINES_PER_LEVEL, BASE_DROP_INTERVAL, MIN_DROP_INTERVAL,
                      DROP_SPEEDUP_PER_LEVEL)
from board import Board
from tetromino import Tetromino
class Game:
    """Holds all Tetris state and implements the game rules."""
    def __init__(self):
        """Create the board and start a fresh game."""
        self.board = Board()
        self.reset()
    def reset(self):
        """(Re)start a fresh game with empty board and zeroed stats."""
        self.board.reset()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.drop_timer = 0
        self.bag = []
        self.next_piece = self._spawn_from_bag()
        self.current_piece = self._new_piece()
    # -- piece supply -------------------------------------------------------
    def _spawn_from_bag(self):
        """7-bag randomizer: all seven shapes shuffled, refilled when empty."""
        if not self.bag:
            self.bag = list(SHAPES.keys())
            random.shuffle(self.bag)
        return Tetromino(self.bag.pop())
    def _new_piece(self):
        """Promote the next piece to current; set game_over if it cannot fit."""
        piece = self.next_piece
        self.next_piece = self._spawn_from_bag()
        if self.board.is_game_over(piece):
            self.game_over = True
        self.current_piece = piece
        return piece
    # -- timing -------------------------------------------------------------
    @property
    def drop_interval(self):
        """Gravity interval in ms, shrinking with level, clamped to minimum."""
        interval = BASE_DROP_INTERVAL - (self.level - 1) * DROP_SPEEDUP_PER_LEVEL
        return max(MIN_DROP_INTERVAL, interval)
    # -- player moves -------------------------------------------------------
    def move_horizontal(self, dx):
        """Shift the piece left/right by dx if the target cells are free."""
        if self.game_over or self.paused:
            return
        if self.board.is_valid_position(self.current_piece, dx=dx):
            self.current_piece.col += dx
    def rotate_piece(self):
        """Rotate clockwise, trying simple wall kicks (0, -1, +1, -2, +2)."""
        if self.game_over or self.paused:
            return
        piece = self.current_piece
        rotated = piece.rotated_matrix()
        for dx in (0, -1, 1, -2, 2):
            if self.board.is_valid_position(piece, dx=dx, matrix=rotated):
                piece.matrix = rotated
                piece.col += dx
                return
    def soft_drop(self):
        """Move down one row (1 pt); lock the piece if it cannot descend."""
        if self.game_over or self.paused:
            return
        if self.board.is_valid_position(self.current_piece, dy=1):
            self.current_piece.row += 1
            self.score += SOFT_DROP_SCORE
        else:
            self._lock_current()
    def hard_drop(self):
        """Drop instantly to the landing spot (2 pts/row), then lock."""
        if self.game_over or self.paused:
            return
        piece = self.current_piece
        dy = 0
        while self.board.is_valid_position(piece, dy=dy + 1):
            dy += 1
        piece.row += dy
        self.score += dy * HARD_DROP_SCORE
        self._lock_current()
    # -- gravity / locking --------------------------------------------------
    def update(self, dt):
        """Advance gravity by dt ms; lock the piece when it can no longer fall."""
        if self.game_over or self.paused:
            return
        self.drop_timer += dt
        while self.drop_timer >= self.drop_interval:
            self.drop_timer -= self.drop_interval
            if self.board.is_valid_position(self.current_piece, dy=1):
                self.current_piece.row += 1
            else:
                self._lock_current()
                break  # a new piece was spawned; discard leftover timer debt
    def _lock_current(self):
        """Lock the piece, clear lines, award score, level up, spawn next."""
        self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        if cleared:
            self.score += LINE_SCORES[cleared] * self.level
            self.lines += cleared
            self.level = self.lines // LINES_PER_LEVEL + 1
        self.drop_timer = 0
        self._new_piece()