'''
board.py
Defines the Board class, which encapsulates the Reversi (Othello) game
board: the 8x8 grid, disc placement, valid-move detection, disc flipping
and score counting. Pure game logic with no user interaction.
'''
from typing import Dict, List, Tuple
# Cell states
EMPTY = 0
BLACK = 1
WHITE = 2
# The eight directions used when searching for flippable discs:
# up, down, left, right and the four diagonals.
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
BOARD_SIZE = 8
Move = Tuple[int, int]
class Board:
    """Represents the Reversi board and implements the game rules."""
    def __init__(self) -> None:
        """Create an empty 8x8 grid and set up the standard starting position."""
        self.size: int = BOARD_SIZE
        self.grid: List[List[int]] = [
            [EMPTY for _ in range(self.size)] for _ in range(self.size)
        ]
        self._setup_initial_position()
    def _setup_initial_position(self) -> None:
        """Place the four starting discs in the centre of the board."""
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE
    def in_bounds(self, row: int, col: int) -> bool:
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def get_cell(self, row: int, col: int) -> int:
        """Return the state (EMPTY/BLACK/WHITE) of the cell at (row, col)."""
        return self.grid[row][col]
    def is_empty(self, row: int, col: int) -> bool:
        """Return True if the cell at (row, col) is empty."""
        return self.grid[row][col] == EMPTY
    @staticmethod
    def get_opponent(player: int) -> int:
        """Return the opponent's colour for the given player colour."""
        return WHITE if player == BLACK else BLACK
    def _flippable_in_direction(
        self, row: int, col: int, d_row: int, d_col: int, player: int
    ) -> List[Move]:
        """
        Walk in one direction from (row, col) collecting opponent discs.
        Return the list of discs that would be flipped if the run of
        opponent discs is terminated by one of the player's own discs;
        return an empty list when the line is broken by an empty cell or
        the edge of the board.
        """
        opponent = self.get_opponent(player)
        flippable: List[Move] = []
        cur_row, cur_col = row + d_row, col + d_col
        while self.in_bounds(cur_row, cur_col):
            cell = self.grid[cur_row][cur_col]
            if cell == opponent:
                flippable.append((cur_row, cur_col))
            elif cell == player:
                return flippable  # line is anchored by one of our discs
            else:  # EMPTY cell breaks the line
                return []
            cur_row += d_row
            cur_col += d_col
        return []  # ran off the board before finding an anchor
    def get_flippable_discs(self, row: int, col: int, player: int) -> List[Move]:
        """
        Return every disc that would be flipped if the player placed a
        disc at (row, col). Returns [] for occupied or off-board cells.
        """
        if not self.in_bounds(row, col) or not self.is_empty(row, col):
            return []
        flippable: List[Move] = []
        for d_row, d_col in DIRECTIONS:
            flippable.extend(self._flippable_in_direction(row, col, d_row, d_col, player))
        return flippable
    def is_valid_move(self, row: int, col: int, player: int) -> bool:
        """A move is valid when the cell is empty and at least one disc flips."""
        return len(self.get_flippable_discs(row, col, player)) > 0
    def get_valid_moves(self, player: int) -> List[Move]:
        """Return a list of every (row, col) move that is valid for the player."""
        return [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
            if self.is_valid_move(row, col, player)
        ]
    def has_valid_move(self, player: int) -> bool:
        """Return True if the player has at least one valid move."""
        return len(self.get_valid_moves(player)) > 0
    def place_disc(self, row: int, col: int, player: int) -> int:
        """
        Place a disc for the player at (row, col) and flip every bracketed
        opponent disc. Return the number of discs flipped.
        Raises ValueError when the move is not legal.
        """
        flippable = self.get_flippable_discs(row, col, player)
        if not flippable:
            raise ValueError(f"Illegal move at ({row}, {col}) for player {player}.")
        self.grid[row][col] = player
        for flip_row, flip_col in flippable:
            self.grid[flip_row][flip_col] = player
        return len(flippable)
    def is_full(self) -> bool:
        """Return True when every cell on the board is occupied."""
        return all(cell != EMPTY for row in self.grid for cell in row)
    def count_discs(self) -> Dict[int, int]:
        """Return a dict mapping BLACK and WHITE to their disc counts."""
        counts: Dict[int, int] = {BLACK: 0, WHITE: 0}
        for row in self.grid:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return counts