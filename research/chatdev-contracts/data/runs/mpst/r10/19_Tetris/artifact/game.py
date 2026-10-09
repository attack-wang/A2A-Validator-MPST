'''
game.py
Core game logic: game state, piece movement/rotation with wall kicks,
gravity, locking, line-clear scoring, and level-based speed progression.
'''
from constants import (LINE_SCORES, SOFT_DROP_POINTS, HARD_DROP_POINTS,
                       LINES_PER_LEVEL, get_drop_interval)
from tetromino import Tetromino, PieceBag
from board import Board
class Game:
    """Manages Tetris game state and rules."""
    def __init__(self):
        """Initialize board, piece bag, score/level state, and first piece."""
        self.board = Board()
        self.bag = PieceBag()
        self.current_piece = None
        self.next_type = self.bag.next_type()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.drop_timer = 0.0
        self.spawn_piece()
    def spawn_piece(self):
        """Create the next tetromino at the top of the board."""
        self.current_piece = Tetromino(self.next_type)
        self.next_type = self.bag.next_type()
        # If a fresh piece already overlaps locked cells, the game is over.
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    def move_left(self):
        """Move the piece one cell left if the target position is valid."""
        if self.board.is_valid_position(self.current_piece, dx=-1):
            self.current_piece.x -= 1
            return True
        return False
    def move_right(self):
        """Move the piece one cell right if the target position is valid."""
        if self.board.is_valid_position(self.current_piece, dx=1):
            self.current_piece.x += 1
            return True
        return False
    def move_down(self):
        """Move the piece one cell down; return True if it moved, False if blocked."""
        if self.board.is_valid_position(self.current_piece, dy=1):
            self.current_piece.y += 1
            return True
        return False
    def rotate(self):
        """
        Rotate the piece 90 degrees clockwise, trying simple wall kicks
        (in place, then nudged left/right/up) so rotations near walls or
        the stack can succeed. Return True if the rotation was applied.
        """
        rotated = self.current_piece.rotated_shape()
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0)):
            if self.board.is_valid_position(self.current_piece, dx, dy, rotated):
                self.current_piece.shape = rotated
                self.current_piece.x += dx
                self.current_piece.y += dy
                return True
        return False
    def hard_drop(self):
        """Drop the piece instantly to its lowest valid position and lock it."""
        distance = 0
        while self.move_down():
            distance += 1
        self.score += distance * HARD_DROP_POINTS
        self.lock_current()
    def soft_drop(self):
        """Move the piece down one cell manually, awarding a small bonus."""
        if self.move_down():
            self.score += SOFT_DROP_POINTS
            self.drop_timer = 0.0  # reset gravity so it does not double-drop
            return True
        return False
    def update(self, dt):
        """
        Advance gravity: accumulate elapsed time and move the piece down
        once per current drop interval; lock it when it can no longer fall.
        """
        if self.game_over:
            return
        self.drop_timer += dt
        interval = get_drop_interval(self.level)
        while self.drop_timer >= interval:
            self.drop_timer -= interval
            if not self.move_down():
                self.lock_current()
                break
    def lock_current(self):
        """Lock the piece, clear lines, update score/level, and spawn the next."""
        self.board.lock_piece(self.current_piece)
        self.drop_timer = 0.0
        lines = self.board.clear_lines()
        self.add_score(lines)
        self.spawn_piece()
    def add_score(self, lines_cleared):
        """Add score for cleared lines and raise the level every 10 lines."""
        if lines_cleared > 0:
            self.score += LINE_SCORES.get(lines_cleared, 800) * self.level
            self.lines += lines_cleared
            self.level = self.lines // LINES_PER_LEVEL + 1