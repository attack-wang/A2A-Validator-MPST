from game import NAMES, STONES


class TerminalUI:
    def show_welcome(self):
        print("=" * 44)
        print("            GOMOKU - Five in a Row")
        print("=" * 44)
        print("Board: 15x15 | Black = X | White = O")
        print("Enter moves as: row col (e.g. '8 8'); 'q' quits.")

    def draw(self, game):
        n = game.size
        print("    " + "".join("{:>3}".format(c + 1) for c in range(n)))
        for r in range(n):
            print("{:>3} ".format(r + 1) + "".join("{:>3}".format(cell) for cell in game.board[r]))
        print()

    def get_move(self, player):
        prompt = "{} ({}) move [row col]: ".format(NAMES[player], STONES[player])
        while True:
            try:
                raw = input(prompt).strip().lower()
            except EOFError:
                print()
                return None
            if raw in ("q", "quit", "exit"):
                return None
            parts = raw.replace(",", " ").split()
            if len(parts) != 2:
                print("Invalid input. Enter two numbers, e.g. '8 8'.")
                continue
            try:
                row, col = int(parts[0]), int(parts[1])
            except ValueError:
                print("Invalid input. Use integers 1-15.")
                continue
            return row - 1, col - 1

    def show_message(self, msg):
        print(msg)