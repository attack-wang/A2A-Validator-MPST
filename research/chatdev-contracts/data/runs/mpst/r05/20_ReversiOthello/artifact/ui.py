'''
ui.py
Console user-interface for the Reversi (Othello) game.
The ConsoleUI class renders the board, highlights legal moves, prints the
running score and safely parses player input such as "d3" or "3 d".
It contains no game rules; it only talks to the Board/Game layers.
'''
from board import BOARD_SIZE, EMPTY, BLACK, WHITE
COLUMN_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
class ConsoleUI:
    """Text-based front-end used to play Reversi in a terminal."""
    SYMBOLS = {EMPTY: '.', BLACK: 'X', WHITE: 'O'}
    LEGAL_MOVE_MARKER = '*'   # marks cells where the current player may play
    # -- output --------------------------------------------------------------
    def display_welcome(self):
        print("=" * 46)
        print("        Welcome to Reversi (Othello)!")
        print("=" * 46)
        print("Black = X, White = O, empty = .")
        print("Legal moves for the player to move are shown as '*'.")
        print("Enter moves as column+row, e.g. 'd3' (or 'quit' to exit).")
        print("-" * 46)
    def display_board(self, board, current_player, valid_moves):
        """Print the board; '*' marks the legal moves of `current_player`."""
        valid_set = set(valid_moves)
        print()
        print("    " + "   ".join(COLUMN_LABELS))
        print("  +" + "---+" * BOARD_SIZE)
        for r in range(BOARD_SIZE):
            cells = []
            for c in range(BOARD_SIZE):
                value = board.grid[r][c]
                if value == EMPTY and (r, c) in valid_set:
                    cells.append(self.LEGAL_MOVE_MARKER)
                else:
                    cells.append(self.SYMBOLS[value])
            print(f"{r + 1} | " + " | ".join(cells) + " |")
            print("  +" + "---+" * BOARD_SIZE)
        turn = self.player_name(current_player) if current_player else "Game over"
        print(f"Turn: {turn}")
    def display_score(self, black, white):
        print(f"Score -> Black (X): {black}   White (O): {white}")
    def display_message(self, message):
        print(message)
    def display_move_result(self, player, row, col, flipped_count):
        name = self.player_name(player)
        coord = self.format_move(row, col)
        print(f"{name} played {coord} and flipped {flipped_count} disc(s).")
    def display_final_result(self, black, white):
        print()
        print("=" * 46)
        print("                 GAME OVER")
        print("=" * 46)
        print(f"Final score -> Black (X): {black}   White (O): {white}")
        if black > white:
            print(f"Black (X) wins by {black - white} disc(s)!")
        elif white > black:
            print(f"White (O) wins by {white - black} disc(s)!")
        else:
            print("It's a tie!")
        print("=" * 46)
    @staticmethod
    def player_name(player):
        return "Black (X)" if player == BLACK else "White (O)"
    @staticmethod
    def format_move(row, col):
        """Convert (row, col) indices into human readable notation, e.g. 'd3'."""
        return f"{COLUMN_LABELS[col]}{row + 1}"
    # -- input ---------------------------------------------------------------
    def parse_move(self, text):
        """
        Parse raw user text.
        Returns:
            'quit'      -> the user asked to quit,
            (row, col)  -> a parsed board coordinate,
            None        -> unrecognised input.
        """
        text = text.strip().lower()
        if text in ('quit', 'exit', 'q'):
            return 'quit'
        compact = text.replace(' ', '').replace(',', '')
        if len(compact) == 2:
            letter, digit = compact[0], compact[1]
            if letter in COLUMN_LABELS and digit in '12345678':
                return int(digit) - 1, COLUMN_LABELS.index(letter)
            if digit in COLUMN_LABELS and letter in '12345678':
                return int(letter) - 1, COLUMN_LABELS.index(digit)
        return None
    def get_move(self, player, valid_moves):
        """
        Prompt `player` for a move until a legal one is entered.
        Returns (row, col) for a legal move, or None if the user quits.
        """
        valid_set = set(valid_moves)
        name = self.player_name(player)
        while True:
            try:
                raw = input(f"{name}, enter your move (e.g. d3): ")
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            parsed = self.parse_move(raw)
            if parsed == 'quit':
                return None
            if parsed is None:
                print("Invalid input. Use a column letter a-h and row 1-8, e.g. 'd3'.")
                continue
            row, col = parsed
            if (row, col) not in valid_set:
                print("That move is not legal. Choose a cell marked with '*'.")
                continue
            return row, col