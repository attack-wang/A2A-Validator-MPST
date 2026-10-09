'''
Board module: implements the Reversi (Othello) game board and its rules,
including valid move detection, disc flipping, and score calculation.
'''
from constants import BOARD_SIZE, EMPTY, BLACK, WHITE
class Board:
    '''
    Represents the 8x8 Reversi board and enforces game rules.
    '''
    def __init__(self):
        '''Initialize the board with the standard Reversi starting position.'''
        self.size = BOARD_SIZE
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self._setup_initial_position()
    def _setup_initial_position(self):
        '''Place the four initial discs in the center of the board.'''
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
    def is_inside_board(self, row, col):
        '''Return True if (row, col) lies within the board boundaries.'''
        return 0 <= row < self.size and 0 <= col < self.size
    def get_disc(self, row, col):
        '''Return the disc (or EMPTY) at the given position.'''
        if self.is_inside_board(row, col):
            return self.grid[row][col]
        return None
    def is_empty_cell(self, row, col):
        '''Return True if the cell is empty and inside the board.'''
        return self.is_inside_board(row, col) and self.grid[row][col] == EMPTY
    def get_opponent(self, player):
        '''Return the opponent of the given player.'''
        return WHITE if player == BLACK else BLACK
    def get_flippable_discs(self, row, col, player):
        '''
        Return a list of (row, col) tuples of opponent discs that would be
        flipped if `player` places a disc at (row, col). Empty if invalid.
        '''
        if not self.is_empty_cell(row, col):
            return []
        opponent = self.get_opponent(player)
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        flippable = []
        for dr, dc in directions:
            path = []
            r, c = row + dr, col + dc
            # Walk in this direction collecting opponent discs
            while self.is_inside_board(r, c) and self.grid[r][c] == opponent:
                path.append((r, c))
                r += dr
                c += dc
            # A valid direction must end on one of the player's own discs
            if path and self.is_inside_board(r, c) and self.grid[r][c] == player:
                flippable.extend(path)
        return flippable
    def is_valid_move(self, row, col, player):
        '''Return True if `player` can legally place a disc at (row, col).'''
        return len(self.get_flippable_discs(row, col, player)) > 0
    def get_valid_moves(self, player):
        '''Return a list of all valid (row, col) moves for `player`.'''
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves
    def place_disc(self, row, col, player):
        '''
        Place a disc for `player` at (row, col) and flip all captured discs.
        Returns the number of discs flipped, or 0 if the move is invalid.
        '''
        flippable = self.get_flippable_discs(row, col, player)
        if not flippable:
            return 0
        self.grid[row][col] = player
        for r, c in flippable:
            self.grid[r][c] = player
        return len(flippable)
    def is_full(self):
        '''Return True if every cell on the board is occupied.'''
        return all(cell != EMPTY for row in self.grid for cell in row)
    def count_discs(self):
        '''
        Return a dictionary mapping each player to the number of discs
        they have on the board.
        '''
        counts = {EMPTY: 0, BLACK: 0, WHITE: 0}
        for row in self.grid:
            for cell in row:
                counts[cell] += 1
        return counts
    def get_score(self):
        '''Return a tuple (black_score, white_score).'''
        counts = self.count_discs()
        return counts[BLACK], counts[WHITE]