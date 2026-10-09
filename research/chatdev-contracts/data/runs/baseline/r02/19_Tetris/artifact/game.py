'''
game.py
Game: state machine, gravity, input actions, scoring, levels, game over.
'''
import random
from constants import (LINE_SCORES, SOFT_DROP_SCORE,
                       HARD_DROP_SCORE, LINES_PER_LEVEL,
                       INITIAL_DROP_INTERVAL, MIN_DROP_INTERVAL, SPEED_FACTOR)
from board import Board
from tetromino import Tetromino
class Game:
    STATE_PLAYING = 'playing'
    STATE_PAUSED = 'paused'
    STATE_GAME_OVER = 'game_over'
    def __init__(self):
        self.reset()
    def reset(self):
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.state = self.STATE_PLAYING
        self.drop_timer = 0.0
        self.next_piece = Tetromino()
        self.current_piece = None
        self.spawn_piece()
    # -- piece management ---
    def spawn_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if not self.board.is_valid_position(self.current_piece.matrix,
                                            self.current_piece.x,
                                            self.current_piece.y):
            self.state = self.STATE_GAME_OVER
    # -- player actions ---
    def move_left(self): self._try_move(-1, 0)
    def move_right(self): self._try_move(1, 0)
    def _try_move(self, dx, dy):
        piece = self.current_piece
        if piece and self.board.is_valid_position(piece.matrix, piece.x + dx, piece.y + dy):
            piece.x += dx
            piece.y += dy
            return True
        return False
    def rotate(self):
        '''Rotate clockwise with simple wall kicks; rotation state is the
        single source of truth (matrix is derived from it).'''
        piece = self.current_piece
        if not piece or self.state != self.STATE_PLAYING:
            return False
        new_rotation = (piece.rotation + 1) % 4
        new_matrix = piece.rotated_matrix()
        for offset in (0, -1, 1, -2, 2):
            if self.board.is_valid_position(new_matrix, piece.x + offset, piece.y):
                piece.rotation = new_rotation
                piece.x += offset
                return True
        return False
    def soft_drop(self):
        if self._try_move(0, 1):
            self.score += SOFT_DROP_SCORE
            self.drop_timer = 0.0
            return True
        return False
    def hard_drop(self):
        piece = self.current_piece
        distance = 0
        while self._try_move(0, 1):
            distance += 1
        self.score += distance * HARD_DROP_SCORE
        self._lock_current()
    def _lock_current(self):
        top_out = self.board.lock_piece(self.current_piece)
        cleared = self.board.clear_lines()
        self._apply_score(cleared)
        if top_out:
            self.state = self.STATE_GAME_OVER
        else:
            self.spawn_piece()
    def _apply_score(self, cleared):
        if cleared:
            self.score += LINE_SCORES.get(cleared, 0) * self.level
            self.lines += cleared
            self.level = 1 + self.lines // LINES_PER_LEVEL
    # -- gravity ---
    def drop_interval(self):
        interval = INITIAL_DROP_INTERVAL * (SPEED_FACTOR ** (self.level - 1))
        return max(interval, MIN_DROP_INTERVAL)
    def update(self, dt):
        if self.state != self.STATE_PLAYING:
            return
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval():
            self.drop_timer = 0.0
            if not self._try_move(0, 1):
                self._lock_current()
    def toggle_pause(self):
        if self.state == self.STATE_PLAYING:
            self.state = self.STATE_PAUSED
        elif self.state == self.STATE_PAUSED:
            self.state = self.STATE_PLAYING
    # -- ghost piece ---
    def ghost_y(self):
        piece = self.current_piece
        if piece is None:
            return 0
        y = piece.y
        while self.board.is_valid_position(piece.matrix, piece.x, y + 1):
            y += 1
        return y