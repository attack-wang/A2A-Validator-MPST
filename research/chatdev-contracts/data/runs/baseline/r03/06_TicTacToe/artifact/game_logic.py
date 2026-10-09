'''
game_logic.py
Core game engine for the Tic-Tac-Toe game.
This module contains the TicTacToe class, which manages the 3x3 board
state, validates player moves, alternates turns between 'X' and 'O',
records the move history, and detects win / draw conditions.
The engine is completely independent of any GUI code, which keeps the
game rules reusable, maintainable, and easy to test.
'''
class TicTacToe:
    """
    Core Tic-Tac-Toe game engine.
    Manages a standard 3x3 board, tracks the current player ('X' or 'O'),
    validates moves, records move history, and determines win/draw outcomes.
    Attributes:
        EMPTY (str): Symbol representing an empty cell.
        board (list[list[str]]): 3x3 grid holding the current game state.
        current_player (str): The player whose turn it is ('X' or 'O').
        game_over (bool): True once the game has ended (win or draw).
        winner (str or None): Winning player's symbol, or None for a draw.
        winning_line (list[tuple[int, int]] or None): Coordinates of the
            three cells forming the winning line (used by the GUI).
        moves_made (int): Total number of valid moves played so far.
        move_history (list[tuple[str, int, int]]): Ordered record of every
            valid move as (player, row, col).
    """
    EMPTY = " "
    PLAYERS = ("X", "O")
    def __init__(self):
        """Initialize a fresh game with an empty board; 'X' moves first."""
        self.reset()
    def reset(self):
        """Reset the board and all game state for a brand-new round."""
        self.board = [[self.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = self.PLAYERS[0]
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.moves_made = 0
        self.move_history = []
    def is_valid_move(self, row, col):
        """
        Check whether placing a mark at (row, col) is legal.
        A move is valid when the indices are within range (0-2), the target
        cell is empty, and the game is not already over.
        Args:
            row (int): Row index (0-2).
            col (int): Column index (0-2).
        Returns:
            bool: True if the move is legal, False otherwise.
        """
        if self.game_over:
            return False
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        return self.board[row][col] == self.EMPTY
    def make_move(self, row, col):
        """
        Attempt to place the current player's mark at (row, col).
        If the move is valid, the mark is written to the board, the move is
        recorded in the history, and win/draw conditions are evaluated.
        If the game continues, the turn switches to the other player.
        Args:
            row (int): Row index (0-2).
            col (int): Column index (0-2).
        Returns:
            bool: True if the move was applied, False if it was rejected.
        """
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        self.move_history.append((self.current_player, row, col))
        self.moves_made += 1
        if self._check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif self.is_board_full():
            self.game_over = True   # Board full with no winner -> draw
            self.winner = None
        else:
            self._switch_player()
        return True
    def _switch_player(self):
        """Alternate the turn between 'X' and 'O'."""
        self.current_player = (
            self.PLAYERS[1] if self.current_player == self.PLAYERS[0]
            else self.PLAYERS[0]
        )
    def _check_winner(self):
        """
        Scan the board for a winning line belonging to the current player.
        Checks all three rows, all three columns, and both diagonals. On
        success, stores the coordinates of the winning cells in
        self.winning_line so the GUI can highlight them.
        Returns:
            bool: True if the current player has completed a line.
        """
        player = self.current_player
        # Rows
        for row in range(3):
            if all(self.board[row][c] == player for c in range(3)):
                self.winning_line = [(row, c) for c in range(3)]
                return True
        # Columns
        for col in range(3):
            if all(self.board[r][col] == player for r in range(3)):
                self.winning_line = [(r, col) for r in range(3)]
                return True
        # Main diagonal (top-left -> bottom-right)
        if all(self.board[i][i] == player for i in range(3)):
            self.winning_line = [(i, i) for i in range(3)]
            return True
        # Anti-diagonal (top-right -> bottom-left)
        if all(self.board[i][2 - i] == player for i in range(3)):
            self.winning_line = [(i, 2 - i) for i in range(3)]
            return True
        return False
    def is_board_full(self):
        """
        Determine whether every cell on the board is occupied.
        Returns:
            bool: True if no empty cells remain, else False.
        """
        return all(
            self.board[r][c] != self.EMPTY
            for r in range(3)
            for c in range(3)
        )
    def is_draw(self):
        """
        Determine whether the finished game ended in a draw.
        A draw occurs when the game is over, the board is full, and there
        is no winner.
        Returns:
            bool: True if the game ended in a draw, else False.
        """
        return self.game_over and self.winner is None
    def get_valid_moves(self):
        """
        List all currently available (empty) cells.
        Returns:
            list[tuple[int, int]]: Coordinates of every empty cell.
        """
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.board[r][c] == self.EMPTY
        ]
    def get_cell(self, row, col):
        """
        Return the symbol currently stored at (row, col).
        Args:
            row (int): Row index (0-2).
            col (int): Column index (0-2).
        Returns:
            str: 'X', 'O', or the EMPTY symbol.
        """
        return self.board[row][col]
    def get_move_history(self):
        """
        Return the ordered history of all valid moves.
        Returns:
            list[tuple[str, int, int]]: Each entry is (player, row, col).
        """
        return list(self.move_history)