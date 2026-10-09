'''
board.py
Pure game-logic module for the Gomoku (Five-in-a-Row) game.
The `Board` class is completely independent of any GUI framework: it only
manages the 15x15 grid, the alternating turns of the black and white
players, win/draw detection and the move history used by the undo feature.
This separation keeps the rules testable and lets the GUI stay thin.
'''
from config import (BOARD_SIZE, EMPTY, PLAYER_BLACK, PLAYER_WHITE)
class Board:
    '''Represents the Gomoku board and enforces the game rules.'''
    # The four directions that need to be inspected for a five-in-a-row:
    # horizontal, vertical and both diagonals.
    DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.reset()
    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------
    def reset(self):
        '''Clear the board and restart the game (black always begins).'''
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = PLAYER_BLACK
        self.move_history = []      # List of (row, col, player) tuples.
        self.winner = None          # None, PLAYER_BLACK or PLAYER_WHITE.
        self.winning_line = None    # List of (row, col) forming the win.
        self.board_full = False     # True when the game ended in a draw.
    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def is_valid_move(self, row, col):
        '''True when (row, col) lies on the board and is still empty.'''
        return (0 <= row < self.size and 0 <= col < self.size
                and self.grid[row][col] == EMPTY)
    def is_full(self):
        '''True when every intersection holds a stone (draw condition).'''
        return len(self.move_history) >= self.size * self.size
    def game_over(self):
        '''True when the game has been won or ended in a draw.'''
        return self.winner is not None or self.board_full
    def last_move(self):
        '''Return the most recent (row, col, player) or None.'''
        if self.move_history:
            return self.move_history[-1]
        return None
    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------
    def place_stone(self, row, col):
        '''
        Attempt to place a stone for the player on turn.
        Returns True when the move was legal and executed. Handles turn
        switching, win detection and the draw condition internally.
        '''
        if self.game_over() or not self.is_valid_move(row, col):
            return False
        player = self.current_player
        self.grid[row][col] = player
        self.move_history.append((row, col, player))
        line = self._find_winning_line(row, col, player)
        if line is not None:
            self.winner = player
            self.winning_line = line
        elif self.is_full():
            self.board_full = True
        else:
            # 3 - player maps PLAYER_BLACK(1) <-> PLAYER_WHITE(2).
            self.current_player = PLAYER_WHITE if player == PLAYER_BLACK else PLAYER_BLACK
        return True
    def undo(self):
        '''
        Take back the most recent move (if any).
        Restores the turn to the player who made that move and clears any
        win/draw state. Returns True when a move was removed.
        '''
        if not self.move_history:
            return False
        row, col, player = self.move_history.pop()
        self.grid[row][col] = EMPTY
        self.current_player = player
        self.winner = None
        self.winning_line = None
        self.board_full = False
        return True
    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _find_winning_line(self, row, col, player):
        '''
        Return the list of (row, col) intersections that form an unbroken
        line of at least five `player` stones through (row, col), or None.
        Both directions of every axis are walked from the freshly placed
        stone, so exactly the contiguous run is collected (it may be longer
        than five stones, e.g. an "overline").
        '''
        for dr, dc in self.DIRECTIONS:
            line = [(row, col)]
            # Walk forwards from the placed stone.
            r, c = row + dr, col + dc
            while (0 <= r < self.size and 0 <= c < self.size
                   and self.grid[r][c] == player):
                line.append((r, c))
                r += dr
                c += dc
            # Walk backwards from the placed stone.
            r, c = row - dr, col - dc
            while (0 <= r < self.size and 0 <= c < self.size
                   and self.grid[r][c] == player):
                line.insert(0, (r, c))
                r -= dr
                c -= dc
            if len(line) >= 5:
                return line
        return None