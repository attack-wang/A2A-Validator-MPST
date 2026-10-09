"""Gomoku: two-player game on a 15x15 board; five in a row wins."""


BOARD_SIZE = 15
EMPTY = "."
BLACK = "X"
WHITE = "O"
DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


class GomokuGame:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.board = [[EMPTY] * size for _ in range(size)]
        self.current = BLACK
        self.winner = None
        self.moves = 0

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def place(self, r, c):
        if self.winner or not self.in_bounds(r, c) or self.board[r][c] != EMPTY:
            return False
        self.board[r][c] = self.current
        self.moves += 1
        if self.check_win(r, c):
            self.winner = self.current
        elif self.moves == self.size * self.size:
            self.winner = "DRAW"
        else:
            self.current = WHITE if self.current == BLACK else BLACK
        return True

    def check_win(self, r, c):
        stone = self.board[r][c]
        for dr, dc in DIRECTIONS:
            count = 1
            for sign in (1, -1):
                nr, nc = r + dr * sign, c + dc * sign
                while self.in_bounds(nr, nc) and self.board[nr][nc] == stone:
                    count += 1
                    nr += dr * sign
                    nc += dc * sign
            if count >= 5:
                return True
        return False

    def render(self):
        header = "   " + " ".join(f"{c:2d}" for c in range(self.size))
        lines = [header]
        for r in range(self.size):
            lines.append(f"{r:2d} " + " ".join(f"{cell:>2}" for cell in self.board[r]))
        return "\n".join(lines)


def parse_move(text):
    parts = text.replace(",", " ").split()
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def read_move(prompt):
    """Read a move line; return None on EOF or interrupt instead of crashing."""
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def main():
    game = GomokuGame()
    print("Gomoku 15x15 - Black (X) moves first.")
    print("Enter moves as 'row col' (integers 0-14), or 'q' to quit.")
    while True:
        print()
        print(game.render())
        if game.winner:
            if game.winner == "DRAW":
                print("Draw - the board is full.")
            else:
                name = "Black" if game.winner == BLACK else "White"
                print(f"{name} ({game.winner}) wins with five in a row!")
            break
        name = "Black" if game.current == BLACK else "White"
        text = read_move(f"{name} ({game.current}) move: ")
        if text is None:
            print("Input stream closed - game aborted.")
            break
        if text in ("q", "quit", "exit"):
            print("Game aborted.")
            break
        move = parse_move(text)
        if move is None or not game.place(*move):
            print("Invalid move. Enter two integers 0-14 for an empty cell.")
    print("Final board:")
    print(game.render())


if __name__ == "__main__":
    main()