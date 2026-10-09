'''
Game module: core Tetris state machine (spawning, gravity, locking, scoring, levels).
'''
import random
from config import (BASE_DROP_INTERVAL, SPEED_FACTOR, MIN_DROP_INTERVAL,
                    LINES_PER_LEVEL, LINE_SCORES, SOFT_DROP_SCORE,
                    HARD_DROP_SCORE)
from board import Board
from tetromino import Tetromino, SHAPES
class Game:
    '''Holds the complete Tetris game state and implements all game actions.'''
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.drop_timer = 0.0
        self._bag = []
        self.current_piece = None
        self.next_piece = self._create_piece()
        self._spawn()
    def _next_shape_name(self):
        '''7-bag randomizer: each of the seven shapes appears once per bag.'''
        if not self._bag:
            self._bag = list(SHAPES.keys())
            random.shuffle(self._bag)
        return self._bag.pop()
    def _create_piece(self):
        '''Create a new tetromino from the 7-bag randomizer, centered at the top.'''
        piece = Tetromino(shape_name=self._next_shape_name())
        piece.x = piece.spawn_position(self.board.width)
        piece.y = -piece.top_offset()
        return piece
    def _spawn(self):
        '''Bring the next piece into play; game over if it cannot be placed.'''
        self.current_piece = self.next_piece
        self.next_piece = self._create_piece()
        if not self.board.can_place(self.current_piece):
            self.game_over = True
    @property
    def drop_interval(self):
        '''Seconds between gravity steps; shrinks as the level increases.'''
        interval = BASE_DROP_INTERVAL * (SPEED_FACTOR ** (self.level - 1))
        return max(MIN_DROP_INTERVAL, interval)
    def update(self, dt):
        '''Advance the game by dt seconds: apply gravity to the current piece.'''
        if self.game_over or self.paused:
            return
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0.0
            self.move_down()
    def move_down(self):
        '''Gravity step: move piece down one row or lock it.'''
        if self.board.can_place(self.current_piece, dy=1):
            self.current_piece.y += 1
        else:
            self._lock_piece()
    def _lock_piece(self):
        '''Lock the current piece, clear lines, update score/level and spawn the next piece.'''
        if not self.board.lock(self.current_piece):
            self.game_over = True  # locked above the board
            return
        cleared = self.board.clear_lines()
        if cleared:
            self.score += LINE_SCORES.get(cleared, 800 * cleared)
            self.lines += cleared
            self.level = 1 + self.lines // LINES_PER_LEVEL
        self._spawn()
    def move_left(self):
        '''Move the piece one column left if possible.'''
        if self.board.can_place(self.current_piece, dx=-1):
            self.current_piece.x -= 1
    def move_right(self):
        '''Move the piece one column right if possible.'''
        if self.board.can_place(self.current_piece, dx=1):
            self.current_piece.x += 1
    def rotate(self):
        '''Rotate clockwise with simple wall kicks; returns True on success.'''
        rotated = self.current_piece.rotated_matrix()
        for dx in (0, -1, 1, -2, 2):
            if self.board.can_place(self.current_piece, dx=dx, matrix=rotated):
                self.current_piece.matrix = rotated
                self.current_piece.x += dx
                return True
        return False
    def soft_drop(self):
        '''Move down one row; award a point if successful.'''
        if self.board.can_place(self.current_piece, dy=1):
            self.current_piece.y += 1
            self.score += SOFT_DROP_SCORE
            self.drop_timer = 0.0
            return True
        return False
    def hard_drop(self):
        '''Drop the piece to the lowest possible position and lock it.'''
        distance = 0
        while self.board.can_place(self.current_piece, dy=1):
            self.current_piece.y += 1
            distance += 1
        self.score += distance * HARD_DROP_SCORE
        self._lock_piece()
    def ghost_y(self):
        '''Return the y offset the piece would land at if dropped (for ghost rendering).'''
        offset = 0
        while self.board.can_place(self.current_piece, dy=offset + 1):
            offset += 1
        return self.current_piece.y + offset
    def toggle_pause(self):
        '''Pause or resume the game.'''
        if not self.game_over:
            self.paused = not self.paused
    def restart(self):
        '''Reset the game to its initial state.'''
        self.__init__()