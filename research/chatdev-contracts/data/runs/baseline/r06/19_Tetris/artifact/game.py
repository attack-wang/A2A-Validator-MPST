'''
game.py
Core game logic: state machine, scoring, levels, gravity and player actions.
'''
from constants import (INITIAL_DROP_DELAY, MIN_DROP_DELAY, DROP_DELAY_STEP,
                       LINES_PER_LEVEL, LINE_SCORES, SOFT_DROP_DELAY)
from board import Board
from tetromino import Tetromino
class Game:
    """Encapsulates the full Tetris game state and rules."""
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.drop_timer = 0
        self.drop_delay = self._drop_delay_for_level(self.level)
        self.current_piece = None
        self.next_piece = None
        self._spawn_piece()
    @staticmethod
    def _drop_delay_for_level(level):
        """Compute gravity delay in ms for the given level."""
        return max(MIN_DROP_DELAY, INITIAL_DROP_DELAY - (level - 1) * DROP_DELAY_STEP)
    def _spawn_piece(self):
        """Bring the next piece into play and prepare a new preview piece."""
        if self.next_piece is None:
            self.next_piece = Tetromino()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if self.board.is_game_over(self.current_piece):
            self.game_over = True
    def update(self, dt):
        """Advance gravity and piece locking; dt is elapsed ms since last update."""
        if self.game_over or self.paused:
            return
        self.drop_timer += dt
        if self.drop_timer >= self.drop_delay:
            self.drop_timer = 0
            self._move_down()
    def _move_down(self):
        """Move the current piece one cell down, locking it if it cannot move."""
        if self.board.is_valid_position(self.current_piece, dy=1):
            self.current_piece.move(0, 1)
        else:
            self._lock_piece()
    def _lock_piece(self):
        """Lock the piece into the board, clear lines, update score and spawn next."""
        lock_out = self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        if cleared:
            self.score += LINE_SCORES.get(cleared, 0) * self.level
            self.lines += cleared
            new_level = self.lines // LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.drop_delay = self._drop_delay_for_level(self.level)
        if lock_out:
            # Standard 'lock out' rule: part of the piece locked above the board
            self.game_over = True
        else:
            self._spawn_piece()
    # --- Player actions -------------------------------------------------
    def move_left(self):
        if self._can_act():
            if self.board.is_valid_position(self.current_piece, dx=-1):
                self.current_piece.move(-1, 0)
    def move_right(self):
        if self._can_act():
            if self.board.is_valid_position(self.current_piece, dx=1):
                self.current_piece.move(1, 0)
    def soft_drop(self):
        """Move down one cell, awarding a point per cell when successful."""
        if self._can_act():
            if self.board.is_valid_position(self.current_piece, dy=1):
                self.current_piece.move(0, 1)
                self.score += 1
            else:
                self._lock_piece()
    def hard_drop(self):
        """Drop the piece to its lowest possible position immediately."""
        if self._can_act():
            distance = 0
            while self.board.is_valid_position(self.current_piece, dy=distance + 1):
                distance += 1
            self.current_piece.move(0, distance)
            self.score += distance * 2
            self._lock_piece()
    def rotate(self):
        """Rotate clockwise with a simple wall-kick attempt."""
        if self._can_act():
            rotated = self.current_piece.rotated_matrix()
            kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0)]
            for dx, dy in kicks:
                if self.board.is_valid_position(self.current_piece, dx=dx, dy=dy, matrix=rotated):
                    self.current_piece.matrix = rotated
                    self.current_piece.move(dx, dy)
                    return
    def _can_act(self):
        return not self.game_over and not self.paused
    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused
    def restart(self):
        """Reset the game to its initial state."""
        self.board.reset()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.drop_timer = 0
        self.drop_delay = self._drop_delay_for_level(self.level)
        self.next_piece = None
        self._spawn_piece()
    def get_ghost_position(self):
        """Return a copy of the current piece positioned at its landing spot."""
        ghost = self.current_piece.copy()
        distance = 0
        while self.board.is_valid_position(self.current_piece, dy=distance + 1):
            distance += 1
        ghost.move(0, distance)
        return ghost