"""Game flow for Reversi (Othello)."""
from board import Board, SIZE


class Game:
    def __init__(self):
        self.board = Board()
        self.current = 'B'

    @staticmethod
    def _name(p):
        return "Black (B)" if p == 'B' else "White (W)"

    def display(self):
        b, w = self.board.score()
        print("\n  " + " ".join(str(c + 1) for c in range(SIZE)))
        for r in range(SIZE):
            print(chr(ord('A') + r) + " " + " ".join(self.board.grid[r]))
        print(f"Score - Black: {b}  White: {w}")
        moves = ", ".join(
            f"{chr(ord('A') + r)}{c + 1}"
            for r, c in self.board.valid_moves(self.current))
        print(f"{self._name(self.current)}'s turn. Valid moves: {moves}")

    def parse_move(self, text):
        text = text.strip().upper()
        if len(text) != 2 or not text[0].isalpha() or not text[1].isdigit():
            return None
        r = ord(text[0]) - ord('A')
        c = int(text[1]) - 1
        return (r, c) if self.board.in_bounds(r, c) else None

    def next_turn(self):
        self.current = 'W' if self.current == 'B' else 'B'

    def over(self):
        return self.board.is_full() or not (
            self.board.has_move('B') or self.board.has_move('W'))

    @staticmethod
    def read_move():
        """Read a move line; return None if the input stream is closed/interrupted."""
        try:
            return input("Move: ").strip()
        except EOFError:
            print("\nInput stream closed.")
        except KeyboardInterrupt:
            print("\nInterrupted.")
        return None

    def play(self):
        print("=== Reversi (Othello) ===")
        print("Enter moves as row letter + column number, e.g. D3. Type 'q' to quit.")
        while not self.over():
            if not self.board.has_move(self.current):
                print(f"{self._name(self.current)} has no valid move. Turn passes.")
                self.next_turn()
                continue
            self.display()
            text = self.read_move()
            if text is None or text.lower() in ('q', 'quit', 'exit'):
                print("Game aborted.")
                return
            move = self.parse_move(text)
            if move is None or not self.board.apply_move(self.current, *move):
                print("Invalid move, try again.")
                continue
            self.next_turn()
        self.display()
        b, w = self.board.score()
        if b > w:
            print(f"Game over. Black wins {b}-{w}!")
        elif w > b:
            print(f"Game over. White wins {w}-{b}!")
        else:
            print(f"Game over. It's a tie {b}-{w}!")