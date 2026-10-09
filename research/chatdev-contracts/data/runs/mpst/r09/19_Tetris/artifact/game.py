'''Core game logic: state machine, piece spawning, movement, scoring, levels.'''
import random
from constants import (BOARD_WIDTH, BASE_DROP_INTERVAL, MIN_DROP_INTERVAL,
                       SPEEDUP_PER_LEVEL, LINE_SCORES, SOFT_DROP_SCORE,
                       HARD_DROP_SCORE, LINES_PER_LEVEL)
from board import Board
from tetromino import Tetromino, BASE_SHAPES, shape_matrix
class Game:
    """Manages Tetris game state, rules, scoring and progression."""
    STATE_PLAYING = 'playing'
    STATE_PAUSED = 'paused'
    STATE_GAME_OVER = 'game_over'
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.state = self.STATE_PLAYING
        self.current_piece = None
        self.next_type = random.choice(list(BASE_SHAPES.keys()))
        self.drop_timer = 0
        self.spawn_piece()
    def spawn_piece(self):
        """Spawn the next piece at the top-center; game over if it can't fit."""
        shape_type = self.next_type
        self.next_type = random.choice(list(BASE_SHAPES.keys()))
        matrix = shape_matrix(shape_type)
        spawn_x = (BOARD_WIDTH - len(matrix[0])) // 2
        self.current_piece = Tetromino(shape_type, spawn_x, 0)
        if self.board.is_top_reached(self.current_piece):
            self.state = self.STATE_GAME_OVER
    def move(self, dx, dy):
        """Try to move the current piece; returns True on success."""
        if self.state != self.STATE_PLAYING or self.current_piece is None:
            return False
        candidate = self.current_piece.moved(dx, dy)
        if self.board.is_valid_position(candidate):
            self.current_piece = candidate
            return True
        return False
    def rotate(self):
        """Try to rotate the current piece clockwise (with simple wall kicks)."""
        if self.state != self.STATE_PLAYING or self.current_piece is None:
            return False
        candidate = self.current_piece.rotated()
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0)):
            kicked = candidate.moved(dx, dy)
            if self.board.is_valid_position(kicked):
                self.current_piece = kicked
                return True
        return False
    def soft_drop(self):
        """Move the piece one row down; award a point. Locks if it can't move."""
        if self.move(0, 1):
            self.score += SOFT_DROP_SCORE
            return True
        self.lock_current_piece()
        return False
    def hard_drop(self):
        """Drop the piece to the lowest valid position instantly and lock it."""
        if self.state != self.STATE_PLAYING or self.current_piece is None:
            return
        distance = 0
        while self.move(0, 1):
            distance += 1
        self.score += distance * HARD_DROP_SCORE
        self.lock_current_piece()
    def lock_current_piece(self):
        """Lock the piece into the board, clear lines, update score/level,
        then spawn the next piece."""
        lock_out = self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        if cleared:
            self.score += LINE_SCORES.get(cleared, 0) * self.level
            self.lines += cleared
            self.level = 1 + self.lines // LINES_PER_LEVEL
        self.current_piece = None
        if lock_out:
            self.state = self.STATE_GAME_OVER
        else:
            self.spawn_piece()
    def update(self, dt):
        """Advance gravity timing; dt is elapsed milliseconds."""
        if self.state != self.STATE_PLAYING:
            return
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval():
            self.drop_timer = 0
            if not self.move(0, 1):
                self.lock_current_piece()
    def drop_interval(self):
        """Milliseconds between automatic drops for the current level."""
        interval = BASE_DROP_INTERVAL - (self.level - 1) * SPEEDUP_PER_LEVEL
        return max(MIN_DROP_INTERVAL, interval)
    def ghost_piece(self):
        """A copy of the current piece dropped to its landing position."""
        if self.current_piece is None:
            return None
        ghost = self.current_piece
        while self.board.is_valid_position(ghost.moved(0, 1)):
            ghost = ghost.moved(0, 1)
        return ghost
    def toggle_pause(self):
        """Pause/resume the game."""
        if self.state == self.STATE_PLAYING:
            self.state = self.STATE_PAUSED
        elif self.state == self.STATE_PAUSED:
            self.state = self.STATE_PLAYING
    def restart(self):
        """Reset the game to a fresh state."""
        self.board.reset()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.state = self.STATE_PLAYING
        self.drop_timer = 0
        self.next_type = random.choice(list(BASE_SHAPES.keys()))
        self.spawn_piece()