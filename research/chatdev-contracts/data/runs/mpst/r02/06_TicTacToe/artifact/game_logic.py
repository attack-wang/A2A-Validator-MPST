'''
game_logic.py
Core game logic for the Tic-Tac-Toe game. This module manages the 3x3
board state, validates player moves, tracks every move made by each
player, alternates turns, and determines the winner or a draw. It is
fully independent of any GUI framework, which keeps the rules easy to
test and reuse.
'''
class TicTacToeGame:
    """
    Encapsulates all rules and state of a two-player Tic-Tac-Toe game.
    Attributes:
        board (list[list[str]]): 3x3 grid holding 'X', 'O', or ' '.
        current_player (str): Mark of the player whose turn it is ('X' or 'O').
        winner (str or None): Mark of the winning player, or None if none yet.
        winning_line (list[tuple[int, int]] or None): Coordinates of the three
            cells forming the winning line, or None if there is no winner.
        move_count (int): Total number of successful moves played so far.
        move_history (list[tuple[str, int, int]]): Ordered record of every
            move as (player_mark, row, col).
        game_over (bool): True once the game has been won or drawn.
    """
    def __init__(self):
        """Initialize a fresh game with an empty board; 'X' moves first."""
        self.reset()
    def reset(self):
        """Reset the board, turn order, move tracking, and flags to start state."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.winning_line = None
        self.move_count = 0
        self.move_history = []
        self.game_over = False
    def is_valid_move(self, row, col):
        """
        Check whether placing a mark at (row, col) is legal.
        Args:
            row (int): Row index (0-2).
            col (int): Column index (0-2).
        Returns:
            bool: True if the indices are in range and the cell is empty.
        """
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        return self.board[row][col] == ' '
    def make_move(self, row, col):
        """
        Attempt to place the current player's mark at (row, col).
        If the move is legal, the mark is written, the move is recorded,
        win/draw conditions are evaluated, and the turn switches to the
        other player.
        Args:
            row (int): Row index (0-2).
            col (int): Column index (0-2).
        Returns:
            bool: True if the move was applied; False if the game is over
                  or the target cell is invalid/occupied.
        """
        if self.game_over or not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        self.move_count += 1
        self.move_history.append((self.current_player, row, col))
        winning_line = self._find_winning_line()
        if winning_line is not None:
            self.winner = self.current_player
            self.winning_line = winning_line
            self.game_over = True
        elif self.is_board_full():
            self.game_over = True  # Board full with no winner -> draw
        else:
            self.switch_player()
        return True
    def _find_winning_line(self):
        """
        Scan all rows, columns, and diagonals for three identical marks.
        Returns:
            list[tuple[int, int]] or None: The three (row, col) cells of the
            winning line, or None if no line is complete.
        """
        lines = []
        # All three rows
        for row in range(3):
            lines.append([(row, 0), (row, 1), (row, 2)])
        # All three columns
        for col in range(3):
            lines.append([(0, col), (1, col), (2, col)])
        # Main diagonal (top-left to bottom-right)
        lines.append([(0, 0), (1, 1), (2, 2)])
        # Anti-diagonal (top-right to bottom-left)
        lines.append([(0, 2), (1, 1), (2, 0)])
        for line in lines:
            marks = [self.board[r][c] for r, c in line]
            if marks[0] != ' ' and marks[0] == marks[1] == marks[2]:
                return line
        return None
    def check_winner(self):
        """
        Return the mark of the player who has a complete line, if any.
        Returns:
            str or None: 'X' or 'O' when a winning line exists, else None.
        """
        line = self._find_winning_line()
        if line is not None:
            return self.board[line[0][0]][line[0][1]]
        return None
    def is_board_full(self):
        """Return True if every cell on the board is occupied."""
        return all(cell != ' ' for row in self.board for cell in row)
    def is_draw(self):
        """Return True if the game ended with a full board and no winner."""
        return self.game_over and self.winner is None
    def switch_player(self):
        """Alternate the current player between 'X' and 'O'."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    def get_current_player(self):
        """Return the mark of the player whose turn it is."""
        return self.current_player
    def get_board(self):
        """
        Return a copy of the board so external code can read the state
        without mutating the internal game data.
        """
        return [row[:] for row in self.board]
    def get_move_history(self):
        """
        Return the ordered list of all moves made in the game.
        Returns:
            list[tuple[str, int, int]]: Each entry is (player_mark, row, col).
        """
        return list(self.move_history)