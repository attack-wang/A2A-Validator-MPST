'''
game.py
Core game logic for Tetris: piece spawning with a 7-bag randomizer,
player movement/rotation with wall kicks, gravity with level-based
speed progression, DAS auto-repeat, lock delay, scoring and the
game-over state.
'''
import random
from constants import (BOARD_WIDTH, BOARD_HEIGHT, SHAPES,
                       LINE_SCORES, SOFT_DROP_SCORE, HARD_DROP_SCORE,
                       LINES_PER_LEVEL, BASE_GRAVITY_MS, GRAVITY_STEP_MS,
                       MIN_GRAVITY_MS, LOCK_DELAY_MS, MAX_LOCK_RESETS,
                       DAS_DELAY, DAS_REPEAT)
from tetromino import Tetromino
from board import Board
class Game:
    """Holds board, current/next pieces, score, level and game state."""
    def __init__(self):
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.bag = []
        self.score = 0
        self.lines = 0
        self.level = 1
        self.state = 'playing'          # 'playing' | 'paused' | 'game_over'
        self.fall_timer = 0
        self.lock_timer = 0
        self.lock_resets = 0
        self.lowest_y = 0
        self.move_dir = 0
        self.move_timer = 0
        self.next_piece = self._new_piece()
        self.spawn_piece()
    # ------------------------------------------------------------------ bag
    def _draw_from_bag(self):
        """7-bag randomizer: shuffle all seven shapes, deal them one by one."""
        if not self.bag:
            self.bag = list(SHAPES.keys())
            random.shuffle(self.bag)
        return self.bag.pop()
    def _new_piece(self):
        return Tetromino(self._draw_from_bag())
    # --------------------------------------------------------------- spawn
    def spawn_piece(self):
        """Bring the next piece into play; game over if it cannot fit."""
        self.current = self.next_piece
        self.next_piece = self._new_piece()
        self.current.x, self.current.y = self.current.get_spawn_position(self.board.width)
        self.fall_timer = 0
        self.lock_timer = 0
        self.lock_resets = 0
        self.lowest_y = self.current.y
        self.move_dir = 0
        self.move_timer = 0
        if not self.board.is_valid(self.current.matrix, self.current.x, self.current.y):
            self.state = 'game_over'
    # ------------------------------------------------------------- gravity
    @property
    def gravity_interval(self):
        """Drop interval in ms, shrinking as the level increases."""
        return max(MIN_GRAVITY_MS,
                   BASE_GRAVITY_MS - (self.level - 1) * GRAVITY_STEP_MS)
    def step_down(self):
        """Gravity tick: move down one row or start/advance the lock timer."""
        if self.board.is_valid(self.current.matrix, self.current.x, self.current.y + 1):
            self.current.y += 1
            self.lock_timer = 0
        # when grounded, update() accumulates lock_timer
    # ------------------------------------------------------------- actions
    def try_move(self, dx, dy):
        """Attempt to shift the piece; returns True on success."""
        if self.board.is_valid(self.current.matrix, self.current.x + dx, self.current.y + dy):
            self.current.x += dx
            self.current.y += dy
            self._on_successful_move()
            return True
        return False
    def try_rotate(self, times=1):
        """Attempt to rotate with simple wall kicks; returns True on success."""
        original = self.current.matrix
        candidate = self.current.rotated_matrix(times)
        kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0), (0, 1)]
        for kx, ky in kicks:
            if self.board.is_valid(candidate, self.current.x + kx, self.current.y + ky):
                self.current.matrix = candidate
                self.current.x += kx
                self.current.y += ky
                self._on_successful_move()
                return True
        return False
    def hard_drop(self):
        """Drop the piece to its lowest valid position and lock immediately."""
        distance = 0
        while self.board.is_valid(self.current.matrix, self.current.x, self.current.y + 1):
            self.current.y += 1
            distance += 1
        self.score += distance * HARD_DROP_SCORE
        self.lock_current()
    def lock_current(self):
        """Lock the piece, clear lines, update score/level and spawn the next."""
        for (bx, by) in self.current.cells():
            if by < 0:
                # A piece locked partly above the visible board: game over.
                self.state = 'game_over'
        lines = self.board.lock_piece(self.current)
        if lines:
            self.score += LINE_SCORES[lines] * self.level
            self.lines += lines
            self.level = self.lines // LINES_PER_LEVEL + 1
        self.spawn_piece()
    def _on_successful_move(self):
        """Reset the lock delay when a grounded piece is moved or rotated."""
        if self.current.y > self.lowest_y:
            self.lowest_y = self.current.y
            self.lock_resets = 0
            self.lock_timer = 0
        elif self.lock_timer > 0 and self.lock_resets < MAX_LOCK_RESETS:
            self.lock_timer = 0
            self.lock_resets += 1
    # -------------------------------------------------------------- update
    def update(self, dt):
        if self.state != 'playing':
            return
        self._handle_held_keys(dt)
        self.fall_timer += dt
        if self.fall_timer >= self.gravity_interval:
            self.fall_timer = 0
            self.step_down()
        grounded = not self.board.is_valid(
            self.current.matrix, self.current.x, self.current.y + 1)
        if grounded:
            self.lock_timer += dt
            if self.lock_timer >= LOCK_DELAY_MS:
                self.lock_current()
        else:
            self.lock_timer = 0
    def _handle_held_keys(self, dt):
        """DAS: immediate move on press, then auto-repeat while held."""
        keys = pygame.key.get_pressed()
        ...