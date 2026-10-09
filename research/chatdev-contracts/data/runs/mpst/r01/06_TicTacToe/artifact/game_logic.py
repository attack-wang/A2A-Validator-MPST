'''
game_logic.py
Core game logic for the two-player Tic-Tac-Toe game.
This module is completely independent of any GUI framework. It manages
the 3x3 board, validates and records each player's move, alternates
turns between 'X' and 'O', detects winning lines and draws, and can
reset the game for a new round.
'''
class GameLogic:
    """Encapsulates the state and rules of a Tic-Tac-Toe match."""
    EMPTY = ' '
    PLAYERS = ('X', 'O')
    # All eight lines that win the game: three rows, three columns,
    # and the two diagonals.
    WINNING_COMBINATIONS = (
        ((0, 0), (0, 1), (0, 2)),  # top row
        ((1, 0), (1, 1), (1, 2)),  # middle row
        ((2, 0), (2, 1), (2, 2)),  # bottom row
        ((0, 0), (1, 0), (2, 0)),  # left column
        ((0, 1), (1, 1), (2, 1)),  # middle column
        ((0, 2), (1, 2), (2, 2)),  # right column
        ((0, 0), (1, 1), (2, 2)),  # main diagonal
        ((0, 2), (1, 1), (2, 0)),  # anti-diagonal
    )
    def __init__(self):
        """Create an empty 3x3 board; player 'X' always moves first."""
        self.reset()
    # ------------------------------------------------------------------
    # Move handling
    # ------------------------------------------------------------------
    def is_valid_move(self, row, col):
        """Return True if (row, col) lies inside the board and is empty."""
        return (
            0 <= row < 3
            and 0 <= col < 3
            and self.board[row][col] == self.EMPTY
        )
    def make_move(self, row, col):
        """
        Place the current player's mark at (row, col).
        The move is recorded only if the game is still running and the
        target cell is empty. Returns True when the move succeeds.
        """
        if self.game_over or not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        self.move_count += 1
        self.move_history.append((self.current_player, row, col))
        return True
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player = (
            self.PLAYERS[1] if self.current_player == self.PLAYERS[0] else self.PLAYERS[0]
        )
    # ------------------------------------------------------------------
    # End-of-game detection
    # ------------------------------------------------------------------
    def check_winner(self):
        """
        Scan every row, column and diagonal for three identical marks.
        When a winning line is found, the winner, the winning
        combination and the game-over flag are recorded and the
        combination is returned. Returns None while nobody has won.
        """
        for combination in self.WINNING_COMBINATIONS:
            marks = [self.board[r][c] for r, c in combination]
            if marks[0] != self.EMPTY and marks[0] == marks[1] == marks[2]:
                self.winner = marks[0]
                self.winning_combination = combination
                self.game_over = True
                return combination
        return None
    def is_board_full(self):
        """Return True when every cell of the board is occupied."""
        return all(
            cell != self.EMPTY for row in self.board for cell in row
        )
    def check_draw(self):
        """
        Return True when the board is full and nobody has won.
        The game-over flag is set so the internal state stays consistent
        even when this module is used without the GUI layer.
        """
        if self.is_board_full() and self.winner is None:
            self.game_over = True
            return True
        return False
    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------
    def get_current_player(self):
        """Return the mark ('X' or 'O') of the player who moves next."""
        return self.current_player
    def get_board(self):
        """Return a copy of the board so callers cannot mutate the state."""
        return [row[:] for row in self.board]
    def get_move_count(self):
        """Return how many moves have been played so far."""
        return self.move_count
    def get_move_history(self):
        """Return the ordered list of (player, row, col) moves played."""
        return list(self.move_history)
    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def reset(self):
        """Clear the board and restore the initial game state."""
        self.board = [[self.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = self.PLAYERS[0]  # 'X' always starts
        self.move_count = 0
        self.move_history = []
        self.winner = None
        self.winning_combination = None
        self.game_over = False