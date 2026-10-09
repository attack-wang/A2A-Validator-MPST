'''
ui.py
This module contains the ConsoleUI class, responsible for all interaction
with the users: drawing the board, showing scores and messages, reading
moves from the keyboard, and announcing the final result.
EOF-safe: reading a move treats a closed/exhausted stdin as a quit request
so the game loop ends cleanly instead of raising EOFError.
'''
from board import EMPTY, BLACK, WHITE, BOARD_SIZE
class ConsoleUI:
    """Text-based user interface for the Reversi game."""
    COLUMN_LABELS = "abcdefgh"
    def display_welcome(self):
        """Print a short welcome banner with instructions."""
        print("=" * 50)
        print("        Welcome to Reversi (Othello)!")
        print("=" * 50)
        print("Black (X) moves first. Enter moves as coordinates,")
        print("e.g. 'd3' or 'row col' like '4 3'. Type 'q' to quit.")
        print("Valid moves are marked with '*'.")
        print("=" * 50)
    def display_board(self, board, valid_moves=None):
        """Draw the board; valid moves are highlighted with '*'."""
        if valid_moves is None:
            valid_moves = []
        hint_cells = set(valid_moves)
        header = "  " + " ".join(self.COLUMN_LABELS[:BOARD_SIZE])
        print(header)
        for row in range(BOARD_SIZE):
            row_str = f"{row + 1} "
            for col in range(BOARD_SIZE):
                cell = board.get_cell(row, col)
                if cell == BLACK:
                    row_str += "X"
                elif cell == WHITE:
                    row_str += "O"
                elif (row, col) in hint_cells:
                    row_str += "*"
                else:
                    row_str += "."
                if col < BOARD_SIZE - 1:
                    row_str += " "
            print(row_str)
        print(header)
    def display_score(self, board, players):
        """Print the current disc counts for both players."""
        counts = board.count_discs()
        black_player = next(p for p in players if p.color == BLACK)
        white_player = next(p for p in players if p.color == WHITE)
        print(f"Score -> {black_player.name} (X): {counts[BLACK]} | "
              f"{white_player.name} (O): {counts[WHITE]}")
    def display_turn(self, player, valid_moves):
        """Announce whose turn it is and how many moves are available."""
        print(f"\n{player.name}'s turn ({player.symbol}). "
              f"Valid moves: {len(valid_moves)}")
    def get_move(self, player, board, valid_moves):
        """
        Prompt the current player for a move until a valid one is entered.
        Accepts algebraic notation ('d3') or 'row col' ('4 3').
        Returns (row, col) as zero-based indices, or None to quit.
        EOF on stdin is treated as a quit request instead of crashing.
        """
        while True:
            try:
                raw = input(f"{player.name}, enter your move: ").strip().lower()
            except EOFError:
                # stdin closed/exhausted (non-interactive environment):
                # treat as a quit request so the game loop ends cleanly.
                return None
            if raw in ("q", "quit", "exit"):
                return None
            parsed = self._parse_move(raw)
            if parsed is None:
                print("Could not understand that. Use 'd3' or '4 3'.")
                continue
            row, col = parsed
            if not board.in_bounds(row, col):
                print("That position is off the board. Try again.")
                continue
            if (row, col) not in valid_moves:
                print("That is not a valid move (no discs would be flipped). Try again.")
                continue
            return row, col
    @staticmethod
    def _parse_move(raw):
        """
        Convert user input to zero-based (row, col).
        Supports 'd3' style and 'row col' style. Returns None on failure.
        """
        raw = raw.replace(",", " ")
        tokens = raw.split()
        if len(tokens) == 1 and len(tokens[0]) >= 2:
            token = tokens[0]
            col_letter, row_part = token[0], token[1:]
            if col_letter in ConsoleUI.COLUMN_LABELS and row_part.isdigit():
                col = ConsoleUI.COLUMN_LABELS.index(col_letter)
                row = int(row_part) - 1
                return row, col
        elif len(tokens) == 2 and all(t.isdigit() for t in tokens):
            row, col = int(tokens[0]) - 1, int(tokens[1]) - 1
            return row, col
        return None
    def display_message(self, message):
        """Print an arbitrary message to the user."""
        print(message)
    def display_move_result(self, player, row, col, flipped):
        """Report the move that was just played and how many discs flipped."""
        notation = f"{self.COLUMN_LABELS[col]}{row + 1}"
        print(f"{player.name} played {notation} and flipped {flipped} disc(s).")
    def display_pass(self, player):
        """Inform that a player must pass because no moves are available."""
        print(f"{player.name} has no valid moves and must pass.")
    def display_game_over(self, board, players):
        """Announce the final score and the winner (or a tie)."""
        counts = board.count_discs()
        black_player = next(p for p in players if p.color == BLACK)
        white_player = next(p for p in players if p.color == WHITE)
        print("\n" + "=" * 50)
        print("GAME OVER!")
        print(f"Final score -> {black_player.name} (X): {counts[BLACK]} | "
              f"{white_player.name} (O): {counts[WHITE]}")
        if counts[BLACK] > counts[WHITE]:
            print(f"The winner is {black_player.name} (Black)!")
        elif counts[WHITE] > counts[BLACK]:
            print(f"The winner is {white_player.name} (White)!")
        else:
            print("It's a tie!")
        print("=" * 50)