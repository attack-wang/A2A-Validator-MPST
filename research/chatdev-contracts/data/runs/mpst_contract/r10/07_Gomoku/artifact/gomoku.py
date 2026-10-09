"""Gomoku game logic: 15x15 board, two players, five-in-a-row wins."""

BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2
WIN_LENGTH = 5

DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))

PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
PLAYER_SYMBOLS = {BLACK: "X", WHITE: "O"}


class GomokuGame:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.current = BLACK
        self.winner = None
        self.moves = 0

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_full(self):
        return self.moves >= self.size * self.size

    def place_stone(self, row, col):
        """Place a stone for the current player. Returns True if the move wins."""
        if not self.in_bounds(row, col) or self.board[row][col] != EMPTY:
            raise ValueError("Invalid move: cell out of bounds or occupied.")
        self.board[row][col] = self.current
        self.moves += 1
        if self.check_win(row, col):
            self.winner = self.current
            return True
        self.current = WHITE if self.current == BLACK else BLACK
        return False

    def check_win(self, row, col):
        """Check whether the stone at (row, col) completes five in a row."""
        player = self.board[row][col]
        for dr, dc in DIRECTIONS:
            count = 1
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while self.in_bounds(r, c) and self.board[r][c] == player:
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= WIN_LENGTH:
                return True
        return False

    def render(self):
        header = "   " + " ".join(str(c % 10) for c in range(self.size))
        lines = [header]
        for r in range(self.size):
            cells = " ".join(
                PLAYER_SYMBOLS.get(self.board[r][c], ".") for c in range(self.size)
            )
            lines.append(f"{r:2d} {cells}")
        return "\n".join(lines)

    def play(self):
        print("Gomoku - first to five in a row wins. Enter moves as 'row col'.")
        while self.winner is None and not self.is_full():
            print()
            print(self.render())
            name = PLAYER_NAMES[self.current]
            raw = input(f"{name}'s move (row col): ").strip()
            try:
                parts = raw.replace(",", " ").split()
                row, col = int(parts[0]), int(parts[1])
                self.place_stone(row, col)
            except (ValueError, IndexError):
                print("Invalid input. Enter two numbers 0-14, e.g. '7 7'.")
        print()
        print(self.render())
        if self.winner is not None:
            print(f"{PLAYER_NAMES[self.winner]} wins!")
        else:
            print("Draw - the board is full.")