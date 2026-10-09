class TicTacToe:
    """Core tic-tac-toe logic: 3x3 board, alternating X/O, win detection."""

    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def place(self, row, col):
        """Place the current player's mark at (row, col). Returns True on success."""
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Return 'X' or 'O' if a player has three in a row, else None."""
        b = self.board
        lines = [b[r] for r in range(3)]                                # rows
        lines += [[b[r][c] for r in range(3)] for c in range(3)]        # columns
        lines.append([b[i][i] for i in range(3)])                       # main diagonal
        lines.append([b[i][2 - i] for i in range(3)])                   # anti-diagonal
        for line in lines:
            if line[0] != " " and line[0] == line[1] == line[2]:
                return line[0]
        return None

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)