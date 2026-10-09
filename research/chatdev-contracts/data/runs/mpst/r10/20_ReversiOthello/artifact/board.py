'''
board.py
Core game-logic for the Reversi (Othello) board.
The Board class stores the 8x8 disc grid and implements all rules of
the game: computing valid moves, placing discs, flipping enclosed
opponent discs and counting the score.
'''
from constants import (BOARD_SIZE, EMPTY, BLACK, WHITE, DIRECTIONS)
class Board:
    '''Represents the 8x8 Reversi board and implements the game rules.'''
    def __init__(self):
        '''Create the board and place the four starting discs.'''
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self._setup_initial_position()
    def _setup_initial_position(self):
        '''Place the standard four starting discs in the centre.'''
        mid = BOARD_SIZE // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the board.'''
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def get_disc(self, row, col):
        '''Return the disc value at (row, col): EMPTY, BLACK or WHITE.'''
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None
    def opponent(self, player):
        '''Return the opponent of the given player.'''
        return WHITE if player == BLACK else BLACK
    def _flips_in_direction(self, row, col, d_row, d_col, player):
        '''Walk in one direction from (row, col) collecting opponent discs.
        Returns the list of discs that would be flipped in this direction,
        or an empty list if the line is not enclosed by a player disc.
        '''
        flips = []
        cur_row, cur_col = row + d_row, col + d_col
        opp = self.opponent(player)
        # Collect contiguous opponent discs
        while self.in_bounds(cur_row, cur_col) and self.grid[cur_row][cur_col] == opp:
            flips.append((cur_row, cur_col))
            cur_row += d_row
            cur_col += d_col
        # The line is valid only if it ends on one of our own discs and
        # contains at least one opponent disc
        if flips and self.in_bounds(cur_row, cur_col) and self.grid[cur_row][cur_col] == player:
            return flips
        return []
    def get_flips(self, row, col, player):
        '''Return every disc that would be flipped if `player` plays (row, col).
        Returns an empty list when the move is not legal.
        '''
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        flips = []
        for d_row, d_col in DIRECTIONS:
            flips.extend(self._flips_in_direction(row, col, d_row, d_col, player))
        return flips
    def is_valid_move(self, row, col, player):
        '''Return True if `player` may place a disc on (row, col).'''
        return len(self.get_flips(row, col, player)) > 0
    def get_valid_moves(self, player):
        '''Return a list of all (row, col) cells that are valid moves for `player`.'''
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves
    def has_valid_move(self, player):
        '''Return True if `player` has at least one valid move.'''
        return len(self.get_valid_moves(player)) > 0
    def place_disc(self, row, col, player):
        '''Place a disc for `player` at (row, col) and flip enclosed discs.
        Returns the list of flipped (row, col) positions, or None when the
        move is illegal (nothing is changed in that case).
        '''
        flips = self.get_flips(row, col, player)
        if not flips:
            return None
        self.grid[row][col] = player
        for f_row, f_col in flips:
            self.grid[f_row][f_col] = player
        return flips
    def is_full(self):
        '''Return True when every cell of the board is occupied.'''
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] == EMPTY:
                    return False
        return True
    def get_score(self):
        '''Return the current score as a dict {BLACK: n_black, WHITE: n_white}.'''
        score = {BLACK: 0, WHITE: 0}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                disc = self.grid[row][col]
                if disc in score:
                    score[disc] += 1
        return score
    def reset(self):
        '''Restore the board to the standard starting position.'''
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self._setup_initial_position()