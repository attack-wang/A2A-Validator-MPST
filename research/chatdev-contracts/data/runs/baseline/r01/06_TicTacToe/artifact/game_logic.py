'''
game_logic.py
This module contains the core game logic for the tic-tac-toe game.
It is completely independent of any GUI framework, which keeps the
game rules testable and reusable.
Classes:
    TicTacToeGame: Manages the board state, player turns, and win/draw detection.
'''
class TicTacToeGame:
    '''
    Encapsulates all rules and state of a two-player tic-tac-toe game.
    The board is represented as a 3x3 list of lists. Empty cells hold
    the empty string ''. Player marks are 'X' and 'O'.
    '''
    def __init__(self):
        '''Initialize a fresh game with an empty board and player 'X' to move first.'''
        self.reset()
    def reset(self):
        '''Reset the board, clear the winner, and set player 'X' as the starting player.'''
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.winning_cells = []
        self.game_over = False
    def make_move(self, row, col):
        '''
        Attempt to place the current player's mark at (row, col).
        The move is accepted only if the game is not over and the target
        cell is empty. On a successful move the turn passes to the other
        player and win/draw conditions are evaluated.
        Args:
            row (int): Row index (0-2).
            col (int): Column index (0-2).
        Returns:
            bool: True if the move was valid and applied, False otherwise.
        '''
        if self.game_over:
            return False
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.board[row][col] != '':
            return False
        self.board[row][col] = self.current_player
        winner, cells = self._evaluate_board()
        if winner:
            self.winner = winner
            self.winning_cells = cells
            self.game_over = True
        elif self.is_board_full():
            self.game_over = True
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    def _evaluate_board(self):
        '''
        Scan rows, columns and diagonals for a completed line.
        Returns:
            tuple: (winner_symbol, winning_cells) if a player has won,
                   otherwise (None, []).
        '''
        # Rows
        for r in range(3):
            if self.board[r][0] != '' and self.board[r][0] == self.board[r][1] == self.board[r][2]:
                return self.board[r][0], [(r, 0), (r, 1), (r, 2)]
        # Columns
        for c in range(3):
            if self.board[0][c] != '' and self.board[0][c] == self.board[1][c] == self.board[2][c]:
                return self.board[0][c], [(0, c), (1, c), (2, c)]
        # Diagonals
        if self.board[0][0] != '' and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0], [(0, 0), (1, 1), (2, 2)]
        if self.board[0][2] != '' and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2], [(0, 2), (1, 1), (2, 0)]
        return None, []
    def is_board_full(self):
        '''Return True if every cell is occupied (used for draw detection).'''
        return all(self.board[r][c] != '' for r in range(3) for c in range(3))
    def get_current_player(self):
        '''Return the symbol ('X' or 'O') of the player who moves next.'''
        return self.current_player
    def get_board(self):
        '''Return a copy of the board so callers cannot mutate internal state directly.'''
        return [row[:] for row in self.board]
    def is_game_over(self):
        '''Return True when a player has won or the board is full (draw).'''
        return self.game_over
    def get_winner(self):
        '''Return the winning symbol, or None if the game was a draw / still running.'''
        return self.winner
    def get_winning_cells(self):
        '''Return the list of (row, col) tuples forming the winning line.'''
        return list(self.winning_cells)