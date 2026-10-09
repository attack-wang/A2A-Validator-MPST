'''
game_logic.py
Core game logic for the tic-tac-toe game.
This module contains the TicTacToeGame class, which manages the 3x3 board,
validates and records each player's moves, alternates turns between
players X and O, and detects win and draw conditions.
'''
class TicTacToeGame:
    """Manages the state and rules of a two-player tic-tac-toe game."""
    def __init__(self):
        """Initialize an empty 3x3 board with player X moving first."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None          # [(row, col), ...] cells of the winning line
        self.moves = {'X': 0, 'O': 0}     # number of moves made by each player
        self.move_history = []            # chronological list of (player, row, col)
    def is_valid_move(self, row, col):
        """Return True if (row, col) is on the board, empty, and game is active."""
        if self.game_over:
            return False
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '
    def make_move(self, row, col):
        """
        Place the current player's mark at (row, col) if the move is valid.
        Records the move, checks for a win or draw, and switches turns.
        Returns:
            True if the move was made, False if it was invalid.
        """
        if not self.is_valid_move(row, col):
            return False
        player = self.current_player
        self.board[row][col] = player
        self.moves[player] += 1
        self.move_history.append((player, row, col))
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.winner = winner
        elif self.check_draw():
            self.game_over = True
            self.winner = None
        else:
            self.switch_player()
        return True
    def switch_player(self):
        """Alternate the current player between X and O."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    def check_winner(self):
        """
        Scan all rows, columns, and diagonals for three identical marks.
        Returns:
            'X' or 'O' if there is a winner, otherwise None.
            When a winner exists, self.winning_line holds its three cells.
        """
        lines = []
        # All rows
        for row in range(3):
            lines.append([(row, 0), (row, 1), (row, 2)])
        # All columns
        for col in range(3):
            lines.append([(0, col), (1, col), (2, col)])
        # Main and anti-diagonal
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(0, 2), (1, 1), (2, 0)])
        for line in lines:
            symbols = [self.board[r][c] for r, c in line]
            if symbols[0] != ' ' and symbols[0] == symbols[1] == symbols[2]:
                self.winning_line = line
                return symbols[0]
        self.winning_line = None
        return None
    def check_draw(self):
        """Return True if every cell is filled and there is no winner."""
        return all(self.board[r][c] != ' ' for r in range(3) for c in range(3))
    def reset(self):
        """Clear the board and restore the initial state for a new game."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.moves = {'X': 0, 'O': 0}
        self.move_history = []