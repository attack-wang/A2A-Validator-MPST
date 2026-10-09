'''
game_logic.py
Contains the core game logic for tic-tac-toe: board state,
move validation, win/draw detection, and turn management.
'''
class TicTacToe:
    '''Manages the tic-tac-toe board state and game rules.'''
    def __init__(self):
        '''Initialize an empty 3x3 board with player X starting.'''
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
    def make_move(self, row, col):
        '''Attempt to place the current player's mark at (row, col).
        Returns True if the move was valid and applied.'''
        if self.game_over:
            return False
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.board[row][col] != ' ':
            return False
        self.board[row][col] = self.current_player
        if self.check_winner():
            self.winner = self.current_player
            self.game_over = True
        elif self.is_board_full():
            self.game_over = True
        else:
            self.switch_player()
        return True
    def switch_player(self):
        '''Alternate the current player between X and O.'''
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    def check_winner(self):
        '''Check all rows, columns, and diagonals for a winning line.
        Returns True if the current player has won.'''
        board = self.board
        # Rows
        for r in range(3):
            if board[r][0] == board[r][1] == board[r][2] != ' ':
                return True
        # Columns
        for c in range(3):
            if board[0][c] == board[1][c] == board[2][c] != ' ':
                return True
        # Diagonals
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return True
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return True
        return False
    def is_board_full(self):
        '''Return True if every cell is occupied (draw condition).'''
        return all(cell != ' ' for row in self.board for cell in row)
    def get_winning_line(self):
        '''Return the coordinates of the winning line if any, else None.'''
        board = self.board
        for r in range(3):
            if board[r][0] == board[r][1] == board[r][2] != ' ':
                return ((r, 0), (r, 2))
        for c in range(3):
            if board[0][c] == board[1][c] == board[2][c] != ' ':
                return ((0, c), (2, c))
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return ((0, 0), (2, 2))
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return ((0, 2), (2, 0))
        return None
    def reset(self):
        '''Reset the board for a new game.'''
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False