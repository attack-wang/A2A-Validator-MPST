'''
game.py
Game class holding the full game state: current/next tetromino, score,
level, lines, gravity timing, and all gameplay actions (move, rotate, drop).
'''
import random
from board import Board
from tetromino import Tetromino, SHAPE_TYPES
from constants import (
    SCORE_SINGLE, SCORE_DOUBLE, SCORE_TRIPLE, SCORE_TETRIS,
    SCORE_SOFT_DROP, SCORE_HARD_DROP, LINES_PER_LEVEL,
    BASE_DROP_INTERVAL, SPEED_FACTOR, MIN_DROP_INTERVAL,
)
class Game:
    """Core Tetris gameplay logic and state, independent of rendering."""
    def __init__(self):
        self.reset()
    def reset(self):
        """Reset the game to its initial state (used for restarting)."""
        self.board = Board()
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.paused = False
        self.current_tetromino = None
        self.next_tetromino = Tetromino()
        self.drop_timer = 0.0
        self._bag = []
        self.spawn_tetromino()
    def _next_from_bag(self):
        """7-bag randomizer: shuffle all seven shapes, yield them in order."""
        if not self._bag:
            bag = SHAPE_TYPES[:]
            random.shuffle(bag)
            self._bag = bag
        return self._bag.pop()
    def spawn_tetromino(self):
        """Move the next tetromino into play and prepare a new preview piece.
        Sets game_over if the new piece cannot be placed."""
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino(self._next_from_bag())
        if not self.board.is_valid_position(self.current_tetromino):
            self.game_over = True
    def move_horizontal(self, dx):
        """Try to move the current piece dx cells sideways."""
        if self.game_over or self.paused or self.current_tetromino is None:
            return False
        if self.board.is_valid_position(self.current_tetromino, dx=dx):
            self.current_tetromino.x += dx
            return True
        return False
    def rotate(self):
        """Rotate clockwise with simple wall kicks (try offsets 0, -1, +1, -2, +2)."""
        if self.game_over or self.paused or self.current_tetromino is None:
            return False
        tetromino = self.current_tetromino
        rotated = tetromino.rotated_matrix()
        for offset in (0, -1, 1, -2, 2):
            if self.board.is_valid_position(tetromino, dx=offset, dy=0, matrix=rotated):
                tetromino.apply_rotation(rotated)
                tetromino.x += offset
                return True
        return False
    def soft_drop(self):
        """Move the piece one row down; award a point. Lock if it can't move."""
        if self.game_over or self.paused or self.current_tetromino is None:
            return False
        if self.board.is_valid_position(self.current_tetromino, dy=1):
            self.current_tetromino.y += 1
            self.score += SCORE_SOFT_DROP
            return True
        self._lock_current()
        return False
    def hard_drop(self):
        """Drop the piece to its lowest valid position instantly; award points."""
        if self.game_over or self.paused or self.current_tetromino is None:
            return
        distance = 0
        while self.board.is_valid_position(self.current_tetromino, dy=1):
            self.current_tetromino.y += 1
            distance += 1
        self.score += distance * SCORE_HARD_DROP
        self._lock_current()
    def _lock_current(self):
        """Lock the piece into the board, clear lines, update score/level,
        and spawn the next piece (or end the game)."""
        self.board.lock_tetromino(self.current_tetromino)
        cleared = self.board.clear_lines()
        if cleared:
            self._apply_line_score(cleared)
        self.current_tetromino = None
        if not self.game_over:
            self.spawn_tetromino()
    def _apply_line_score(self, cleared):
        """Add score for cleared lines and advance level every LINES_PER_LEVEL."""
        table = {1: SCORE_SINGLE, 2: SCORE_DOUBLE, 3: SCORE_TRIPLE, 4: SCORE_TETRIS}
        self.score += table.get(cleared, cleared * SCORE_TETRIS) * self.level
        self.lines += cleared
        self.level = self.lines // LINES_PER_LEVEL + 1
    def get_drop_interval(self):
        """Seconds between automatic gravity drops at the current level."""
        interval = BASE_DROP_INTERVAL * (SPEED_FACTOR ** (self.level - 1))
        return max(MIN_DROP_INTERVAL, interval)
    def update(self, dt):
        """Advance gravity by dt seconds; drop/lock the piece when the timer
        exceeds the current drop interval."""
        if self.game_over or self.paused:
            return
        self.drop_timer += dt
        interval = self.get_drop_interval()
        while self.drop_timer >= interval:
            self.drop_timer -= interval
            if self.current_tetromino is None:
                break
            if self.board.is_valid_position(self.current_tetromino, dy=1):
                self.current_tetromino.y += 1
            else:
                self._lock_current()
                break
    def get_ghost_y(self):
        """Row offset where the current piece would land if hard-dropped."""
        if self.current_tetromino is None:
            return None
        tetromino = self.current_tetromino
        dy = 0
        while self.board.is_valid_position(tetromino, dy=dy + 1):
            dy += 1
        return tetromino.y + dy