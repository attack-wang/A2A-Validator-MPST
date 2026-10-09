"""Tic-Tac-Toe game logic: 3x3 board, turn tracking, win/draw detection."""


class TicTacToe:
    """Standard 3x3 tic-tac-toe game with move tracking and win detection."""

    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]

    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.moves = []  # history of (player, index) tuples

    @staticmethod
    def display_guide():
        """Show the coordinate layout so players know how to enter moves."""
        print("\nCell coordinates:")
        print(" 1,1 | 1,2 | 1,3 ")
        print("-----+-----+-----")
        print(" 2,1 | 2,2 | 2,3 ")
        print("-----+-----+-----")
        print(" 3,1 | 3,2 | 3,3 \n")

    def display(self):
        b = self.board
        print(f" {b[0]} | {b[1]} | {b[2]} ")
        print("---+---+---")
        print(f" {b[3]} | {b[4]} | {b[5]} ")
        print("---+---+---")
        print(f" {b[6]} | {b[7]} | {b[8]} ")
        print()

    def position_to_index(self, position):
        """Convert 'row,col' (each 1-3) to a board index, or None if invalid."""
        try:
            parts = position.replace(" ", "").split(",")
            if len(parts) != 2:
                return None
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            return None
        if not (1 <= row <= 3 and 1 <= col <= 3):
            return None
        return (row - 1) * 3 + (col - 1)

    def is_valid_move(self, index):
        """A move is valid if the index is on the board and the cell is empty."""
        return 0 <= index <= 8 and self.board[index] == " "

    def make_move(self, index):
        """Place the current player's mark at index. Returns True on success."""
        if not self.is_valid_move(index):
            return False
        self.board[index] = self.current_player
        self.moves.append((self.current_player, index))
        return True

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Return 'X' or 'O' if that player has three in a row, else None."""
        for a, b, c in self.WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_full(self):
        return " " not in self.board

    def is_over(self):
        return self.check_winner() is not None or self.is_full()

    def move_history(self):
        """Return the tracked moves as readable 'X->(row,col)' strings."""
        return [
            f"{player}->({index // 3 + 1},{index % 3 + 1})"
            for player, index in self.moves
        ]