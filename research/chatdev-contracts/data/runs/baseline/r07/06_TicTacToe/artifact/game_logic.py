'''
game_logic.py
Core game logic for the Tic-Tac-Toe application.
Pure rules engine with no UI code. Provides the TicTacToeGame class that
manages a standard 3x3 board, tracks each player's moves (X and O take
turns), detects wins across rows, columns and diagonals, records the
winning line, detects draws when the board is full, and exposes the full
interface consumed by gui.py: board, current_player, game_over, winner,
winning_line, make_move(row, col), reset() and get_status_message().
'''
class TicTacToeGame:
    """
    Rules engine for a standard 3x3 Tic-Tac-Toe game.
    Attributes:
        board (list[list[str]]): 3x3 grid holding 'X', 'O' or ' ' per cell.
        current_player (str): 'X' or 'O'; the player to move next.
        game_over (bool): True once the game has been won or drawn.
        winner (str | None): 'X' or 'O' on a win, None on a draw or while
            the game is still running.
        winning_line (list[tuple[int, int]] | None): Coordinates of the
            three cells forming the winning line, else None.
    """
    BOARD_SIZE = 3
    EMPTY = " "
    def __init__(self):
        """Initialise a fresh board with player X moving first."""
        self._init_state()
    def _init_state(self):
        """(Re)set all game-state fields to a brand-new game."""
        self.board = [[self.EMPTY for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.BOARD_SIZE)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.winning_line = None
    def make_move(self, row, col):
        """
        Attempt to place the current player's mark at (row, col).
        The move is rejected if the game is already over, the coordinates
        are out of range, or the target cell is already occupied.
        Args:
            row (int): Row index (0-2).
            col (int): Column index (0-2).
        Returns:
            bool: True if the move was valid and applied, otherwise False.
        """
        if self.game_over:
            return False
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return False
        if self.board[row][col] != self.EMPTY:
            return False
        self.board[row][col] = self.current_player
        if self._check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif self._is_board_full():
            self.game_over = True  # Draw: winner remains None
        else:
            self._switch_player()
        return True
    def reset(self):
        """Restore a fresh game state so a new game can begin (X starts)."""
        self._init_state()
    def get_status_message(self):
        """
        Build a human-readable status message for the GUI status bar.
        Returns:
            str: A win, draw, or turn message depending on game state.
        """
        if self.game_over:
            if self.winner:
                return f"Player {self.winner} wins!"
            return "It's a draw!"
        return f"Player {self.current_player}'s turn"
    # --- internal helpers -------------------------------------------------
    def _switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player = "O" if self.current_player == "X" else "X"
    def _is_board_full(self):
        """Return True when every cell has been played (no empty cells)."""
        return all(cell != self.EMPTY
                   for row in self.board for cell in row)
    def _check_winner(self):
        """
        Check all rows, columns and diagonals for a completed line.
        On success, stores the winning coordinates in self.winning_line
        so the GUI can highlight the winning cells.
        Returns:
            bool: True if the current player has completed a line.
        """
        lines = []
        for i in range(self.BOARD_SIZE):
            lines.append([(i, c) for c in range(self.BOARD_SIZE)])   # rows
            lines.append([(r, i) for r in range(self.BOARD_SIZE)])   # columns
        lines.append([(i, i) for i in range(self.BOARD_SIZE)])                        # main diagonal
        lines.append([(i, self.BOARD_SIZE - 1 - i) for i in range(self.BOARD_SIZE)])  # anti-diagonal
        for line in lines:
            marks = [self.board[r][c] for r, c in line]
            if marks[0] != self.EMPTY and marks[0] == marks[1] == marks[2]:
                self.winning_line = line
                return True
        return False