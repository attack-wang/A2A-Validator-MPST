'''
game.py
Contains the Game class which manages the Reversi game flow: turn taking,
input handling, move application, pass handling, score display and the
end-of-game detection / final result.
'''
from board import Board
from player import Player
class Game:
    """Orchestrates a two-player (hot-seat) game of Reversi."""
    def __init__(self, player1_name="Player 1", player2_name="Player 2"):
        self.board = Board()
        self.players = {
            Board.BLACK: Player(player1_name, Board.BLACK),
            Board.WHITE: Player(player2_name, Board.WHITE),
        }
        self.current_color = Board.BLACK  # Black always starts in Othello
    @property
    def current_player(self):
        return self.players[self.current_color]
    def switch_turn(self):
        """Hand the turn over to the other player."""
        self.current_color = self.board.opponent(self.current_color)
    def display_score(self):
        """Print the current disc count for both players."""
        black, white = self.board.count_discs()
        b_name = self.players[Board.BLACK].name
        w_name = self.players[Board.WHITE].name
        print(f"SCORE  {b_name} (B): {black}   |   {w_name} (W): {white}")
    def parse_input(self, text):
        """
        Convert user input into a (row, col) tuple using 0-based indices,
        or None if the input could not be parsed.
        Accepted formats:
            "3 5", "3,5", "(3,5)"  -> row 3, col 5   (1-based numbers)
            "d3", "3d"             -> column D, row 3 (chess-like notation)
        """
        text = text.strip().lower()
        if not text:
            return None
        # Format 1: two numbers separated by space/comma.
        parts = text.replace(',', ' ').replace('(', ' ').replace(')', ' ').split()
        if len(parts) == 2 and all(p.isdigit() for p in parts):
            row, col = int(parts[0]), int(parts[1])
            if 1 <= row <= Board.SIZE and 1 <= col <= Board.SIZE:
                return (row - 1, col - 1)
            return None
        # Format 2: letter+digit, e.g. "d3" or "3d".
        if len(text) == 2:
            if text[0].isalpha() and text[1].isdigit():
                col = ord(text[0]) - ord('a')
                row = int(text[1]) - 1
            elif text[0].isdigit() and text[1].isalpha():
                row = int(text[0]) - 1
                col = ord(text[1]) - ord('a')
            else:
                return None
            if self.board.in_bounds(row, col):
                return (row, col)
        return None
    @staticmethod
    def format_move(move):
        """Format a 0-based (row, col) tuple as chess-like notation, e.g. (2, 3) -> 'D3'."""
        row, col = move
        return f"{chr(ord('A') + col)}{row + 1}"
    def get_move(self, valid_moves):
        """
        Prompt the current player for a move until a valid one is entered.
        Returns the chosen (row, col) 0-based tuple, or None if the player
        typed 'q' to quit the game.
        """
        valid_set = set(valid_moves)
        while True:
            prompt = (f"{self.current_player.name} ({self.current_player.color_name}), "
                      f"your move (e.g. 'd3' or '4 5'), 'h' for help, 'q' to quit: ")
            text = input(prompt).strip()
            if text.lower() in ('q', 'quit', 'exit'):
                return None
            if text.lower() in ('h', 'help'):
                self.show_help()
                continue
            if text.lower() in ('m', 'moves'):
                print("Valid moves: " + ", ".join(self.format_move(m) for m in valid_moves))
                continue
            move = self.parse_input(text)
            if move is None:
                print("  ! Could not understand that input. Use column letter + row number "
                      "(e.g. 'd3') or 'row col' (e.g. '4 5').")
                continue
            if move not in valid_set:
                print(f"  ! ({self.format_move(move)}) is not a valid move for you. "
                      f"Valid moves are marked '*' on the board.")
                continue
            return move
    @staticmethod
    def show_help():
        print("""
HOW TO PLAY:
  * Black moves first; players alternate turns.
  * Enter your move as a column letter + row number (e.g. 'd3')
    or as 'row column' numbers (e.g. '4 5').
  * A valid move must flank one or more of the opponent's discs
    between the new disc and another of your own discs; all
    flanked discs are flipped to your color.
  * Valid squares are marked with '*' on the board.
  * If a player has no valid move, the turn is passed automatically.
  * The game ends when the board is full or neither player can move.
  * Commands: 'm' = list valid moves, 'h' = help, 'q' = quit.
""")
    def show_final_results(self):
        black, white = self.board.count_discs()
        print("\n" + "=" * 60)
        print("GAME OVER!")
        print("=" * 60)
        self.board.display()
        b = self.players[Board.BLACK]
        w = self.players[Board.WHITE]
        print(f"Final score: {b.name} (Black): {black}   |   {w.name} (White): {white}")
        if black > white:
            winner = b
        elif white > black:
            winner = w
        else:
            winner = None
        if winner:
            print(f"THE WINNER IS: {winner.name} ({winner.color_name})!")
        else:
            print("The game ends in a DRAW!")
        print("=" * 60)
    def play(self):
        """Run the main game loop until the game ends or a player quits."""
        print("\n*** Game started! Black moves first. ***")
        while True:
            if self.board.is_full():
                break
            valid_moves = self.board.get_valid_moves(self.current_color)
            if not valid_moves:
                # Game ends when NEITHER player has a valid move.
                if not self.board.has_valid_moves(self.board.opponent(self.current_color)):
                    break
                print(f"\n{self.current_player.name} ({self.current_player.color_name}) "
                      f"has no valid move -- turn passed.")
                self.switch_turn()
                continue
            self.board.display(valid_moves)
            self.display_score()
            move = self.get_move(valid_moves)
            if move is None:
                print("\nGame quit by player. Goodbye!")
                return
            self.board.apply_move(move[0], move[1], self.current_color)
            self.switch_turn()
        self.show_final_results()