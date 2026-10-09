'''
game_logic.py
Core game logic for the 2048 game.
This module contains the Game2048 class, which encapsulates all the
state and rules of a standard 2048 game on a 4x4 grid:
- Board representation as a 2D list of integers (0 means empty).
- Sliding and merging of tiles in four directions (up/down/left/right)
  triggered by arrow keys.
- Spawning a new tile (2 or 4) in a random empty cell after each valid move.
- Score tracking: every merge adds the value of the newly created tile.
- Highest tile tracking.
- Game-over detection: the game ends when no move is possible.
This module is completely independent of any GUI framework so it can be
unit-tested or reused with other front-ends.
Fix: _inverse_transform_board for the 'down' direction now correctly
applies "reverse each row, then transpose" (the previous version reused
the forward transform, which is not self-inverse and corrupted the board
on every down move).
'''
import random
class Game2048:
    """Encapsulates the state and rules of a standard 2048 game."""
    def __init__(self, size=4):
        """Initialize a new game with an empty `size` x `size` board."""
        self.size = size
        self.reset()
    def reset(self):
        """Reset the board, score and game-over flag, then spawn two tiles."""
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self._add_random_tile()
        self._add_random_tile()
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def move(self, direction):
        """
        Slide and merge all tiles in the given direction.
        Parameters
        ----------
        direction : str
            One of 'up', 'down', 'left', 'right'.
        Returns
        -------
        bool
            True if the board changed (a valid move was made), False otherwise.
        """
        if self.game_over:
            return False
        # Work on a transformed copy so every direction can be handled as a
        # "move to the left" on plain rows.
        transformed = self._transform_board(direction, self.board)
        moved = False
        gained = 0
        new_rows = []
        for row in transformed:
            new_row, row_gained, row_moved = self._slide_and_merge_row(row)
            gained += row_gained
            if row_moved:
                moved = True
            new_rows.append(new_row)
        if not moved:
            return False
        self.board = self._inverse_transform_board(direction, new_rows)
        self.score += gained
        # A new tile appears after every successful move.
        self._add_random_tile()
        # Update game-over status.
        self.game_over = self._is_board_stuck(self.board)
        return True
    def get_board(self):
        """Return a deep copy of the current board."""
        return [row[:] for row in self.board]
    def get_score(self):
        """Return the current score."""
        return self.score
    def get_highest_tile(self):
        """Return the highest tile value currently on the board."""
        return max(max(row) for row in self.board)
    def is_game_over(self):
        """Return True when no further move is possible."""
        return self.game_over
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _add_random_tile(self):
        """Spawn a new tile (2 with 90% chance, 4 with 10%) in a random empty cell."""
        empty_cells = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == 0
        ]
        if not empty_cells:
            return
        r, c = random.choice(empty_cells)
        self.board[r][c] = 2 if random.random() < 0.9 else 4
    @staticmethod
    def _slide_and_merge_row(row):
        """
        Slide a single row to the left and merge equal neighbours.
        Returns (new_row, score_gained, moved).
        """
        # Collect non-zero tiles in order.
        tiles = [v for v in row if v != 0]
        merged = []
        gained = 0
        i = 0
        while i < len(tiles):
            # Merge a pair of equal adjacent tiles (each tile merges once).
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                value = tiles[i] * 2
                merged.append(value)
                gained += value
                i += 2
            else:
                merged.append(tiles[i])
                i += 1
        # Pad with zeros back to the original length.
        new_row = merged + [0] * (len(row) - len(merged))
        moved = new_row != list(row)
        return new_row, gained, moved
    def _transform_board(self, direction, board):
        """Transform the board so the requested move becomes a left move."""
        if direction == 'left':
            return [row[:] for row in board]
        if direction == 'right':
            return [row[::-1] for row in board]
        if direction == 'up':
            return [list(col) for col in zip(*board)]
        if direction == 'down':
            transposed = [list(col) for col in zip(*board)]
            return [row[::-1] for row in transposed]
        raise ValueError("direction must be 'up', 'down', 'left' or 'right'")
    def _inverse_transform_board(self, direction, board):
        """Apply the inverse of `_transform_board` to write results back."""
        if direction == 'left':
            return [row[:] for row in board]
        if direction == 'right':
            return [row[::-1] for row in board]
        if direction == 'up':
            return [list(col) for col in zip(*board)]
        if direction == 'down':
            # The 'down' transform is "transpose, then reverse each row".
            # Its inverse is therefore "reverse each row, then transpose"
            # (this transform is NOT self-inverse, unlike the others).
            reversed_rows = [row[::-1] for row in board]
            return [list(col) for col in zip(*reversed_rows)]
        raise ValueError("direction must be 'up', 'down', 'left' or 'right'")
    def _is_board_stuck(self, board):
        """Return True if no move (in any direction) is possible on `board`."""
        # Any empty cell means a move is still possible.
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == 0:
                    return False
        # Otherwise, check for horizontally/vertically adjacent equal tiles.
        for r in range(self.size):
            for c in range(self.size):
                value = board[r][c]
                if c + 1 < self.size and board[r][c + 1] == value:
                    return False
                if r + 1 < self.size and board[r + 1][c] == value:
                    return False
        return True