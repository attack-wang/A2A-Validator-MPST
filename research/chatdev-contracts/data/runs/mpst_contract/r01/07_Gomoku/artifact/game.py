from board import Board, BLACK, WHITE


class Game:
    def __init__(self):
        self.board = Board()
        self.current = BLACK

    def player_name(self):
        return "Black (X)" if self.current == BLACK else "White (O)"

    def parse_move(self, text):
        parts = text.replace(",", " ").split()
        if len(parts) != 2:
            return None
        try:
            r, c = int(parts[0]) - 1, int(parts[1]) - 1
        except ValueError:
            return None
        return (r, c)

    def run(self):
        print("Gomoku: Black (X) vs White (O) on a 15x15 board.")
        print("Enter moves as 'row col' (1-15), or 'q' to quit.")
        while True:
            self.board.display()
            move = input(f"{self.player_name()}, enter move: ").strip().lower()
            if move in ("q", "quit", "exit"):
                print("Game aborted.")
                return
            pos = self.parse_move(move)
            if pos is None or not self.board.is_empty(*pos):
                print("Invalid or occupied cell. Try again.")
                continue
            r, c = pos
            self.board.place(r, c, self.current)
            if self.board.check_win(r, c):
                self.board.display()
                print(f"{self.player_name()} wins with five in a row!")
                return
            if self.board.is_full():
                self.board.display()
                print("Draw! The board is full.")
                return
            self.current = WHITE if self.current == BLACK else BLACK