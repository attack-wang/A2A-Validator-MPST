from board import Board, BLACK
import ui


class Game:
    """Controls turn order, move input, passing and game-over detection."""

    def __init__(self):
        self.board = Board()
        self.current = BLACK

    def run(self):
        print("Reversi (Othello) - X (Black) moves first.")
        print("Enter a move as column+row, e.g. 'd3'. '*' marks valid squares. 'q' quits.")
        while True:
            moves = self.board.valid_moves(self.current)
            print(ui.render(self.board, self.current, moves))
            if not moves:
                opponent = 3 - self.current
                if self.board.is_full() or not self.board.valid_moves(opponent):
                    break
                print(f"{ui.player_name(self.current)} has no valid move - turn passes.")
                self.current = opponent
                continue
            try:
                text = input(f"{ui.player_name(self.current)} move: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGame aborted.")
                return
            if text.strip().lower() in ("q", "quit", "exit"):
                print("Game aborted.")
                return
            pos = ui.parse_move(text)
            if pos is None or not self.board.is_valid_move(pos[0], pos[1], self.current):
                print("Invalid move - try again.")
                continue
            self.board.place(pos[0], pos[1], self.current)
            self.current = 3 - self.current
        black, white = self.board.score()
        print(ui.render(self.board, self.current, []))
        print("Game over.")
        if black > white:
            print(f"X (Black) wins {black}-{white}!")
        elif white > black:
            print(f"O (White) wins {white}-{black}!")
        else:
            print(f"It is a tie: {black}-{white}.")