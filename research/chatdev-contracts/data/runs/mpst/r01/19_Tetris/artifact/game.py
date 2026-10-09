'''
Defines the Game class: the full game state and rules — piece spawning,
movement/rotation with wall kicks, gravity with progressive speed,
line-clear scoring and the game-over condition.
'''
from constants import (
    BASE_DROP_INTERVAL, HARD_DROP_SCORE, LINE_SCORES, LINES_PER_LEVEL,
    MIN_DROP_INTERVAL, ROTATION_KICKS, SOFT_DROP_SCORE, SPEED_FACTOR,
)
from board import Board
from tetromino import Tetromino
class Game:
    """Holds and advances all Tetris game state."""
    def __init__(self):
        """Start a fresh game: empty board, first pieces and zeroed stats."""
        self.board = Board()
        self.next_piece = Tetromino()
        self.current_piece = None
        self.score = 0
        self.lines = 0
        self.level = 1
        self.drop_timer = 0.0
        self.game_over = False
        self.spawn_piece()
    # ----- Difficulty / speed -----
    @property
    def drop_interval(self):
        """Seconds between automatic gravity drops at the current level."""
        interval = BASE_DROP_INTERVAL * (SPEED_FACTOR ** (self.level - 1))
        return max(MIN_DROP_INTERVAL, interval)
    # ----- Piece lifecycle -----
    def spawn_piece(self):
        """Move the queued next piece into play and queue a new one."""
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        # If the fresh piece already overlaps locked blocks, the board is
        # full and the game is over.
        if not self.board.is_valid_position(self.current_piece.get_cells()):
            self.game_over = True
    def lock_current(self):
        """Lock the current piece, clear lines, award points and spawn the next piece."""
        locked_out = self.board.lock_piece(self.current_piece)
        if locked_out:
            self.game_over = True
            return
        cleared = self.board.clear_lines()
        if cleared:
            self.lines += cleared
            self.score += LINE_SCORES.get(cleared, 0) * self.level
            self.level = self.lines // LINES_PER_LEVEL + 1
        self.spawn_piece()
    # ----- Player actions -----
    def move(self, dx, dy):
        """Try to translate the current piece; returns True on success."""
        if self.game_over or self.current_piece is None:
            return False
        cells = self.current_piece.get_cells(dx=dx, dy=dy)
        if self.board.is_valid_position(cells):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    def rotate(self):
        """
        Try to rotate the current piece clockwise, applying simple wall-kick
        offsets so rotations near walls/floor can still succeed.
        """
        if self.game_over or self.current_piece is None:
            return False
        piece = self.current_piece
        rotated = piece.rotated_matrix()
        for dx, dy in ROTATION_KICKS:
            cells = piece.get_cells(dx=dx, dy=dy, matrix=rotated)
            if self.board.is_valid_position(cells):
                piece.apply_matrix(rotated)
                piece.x += dx
                piece.y += dy
                return True
        return False
    def soft_drop(self):
        """Move the piece one row down, awarding a small score bonus."""
        if self.move(0, 1):
            self.score += SOFT_DROP_SCORE
            return True
        return False
    def hard_drop(self):
        """Instantly drop the piece as far as possible, lock it and score."""
        distance = 0
        while self.move(0, 1):
            distance += 1
        self.score += distance * HARD_DROP_SCORE
        self.lock_current()
    # ----- Ghost / preview helpers -----
    def ghost_drop_distance(self):
        """Rows the current piece could fall before landing (for the ghost preview)."""
        if self.game_over or self.current_piece is None:
            return 0
        distance = 0
        while self.board.is_valid_position(
                self.current_piece.get_cells(dx=0, dy=distance + 1)):
            distance += 1
        return distance
    # ----- Frame update -----
    def update(self, dt):
        """
        Advance gravity: accumulate elapsed time and drop the piece whenever
        the level-dependent drop interval elapses. Locks the piece when it
        can no longer move down.
        """
        if self.game_over or self.current_piece is None:
            return
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0.0
            if not self.move(0, 1):
                self.lock_current()