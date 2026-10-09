'''
game.py
This module defines the Game class, which orchestrates a full Reversi
match: turn management, pass handling, end-of-game detection, and the
main play loop that ties the board and the UI together.
'''
from board import Board, BLACK, WHITE
from player import Player
from ui import ConsoleUI
class Game:
    """Controls the flow of a complete Reversi game."""
    def __init__(self, black_name="Player 1", white_name="Player 2"):
        """Create the board, the two players and the console UI."""
        self.board = Board()
        self.players = {
            BLACK: Player(black_name, BLACK),
            WHITE: Player(white_name, WHITE),
        }
        self.ui = ConsoleUI()
        self.current_color = BLACK  # Black always starts
    @property
    def current_player(self):
        """Return the Player whose turn it currently is."""
        return self.players[self.current_color]
    def switch_turn(self):
        """Hand the turn over to the other player."""
        self.current_color = WHITE if self.current_color == BLACK else BLACK
    def is_game_over(self):
        """
        The game ends when the board is full or neither player can move.
        """
        if self.board.is_full():
            return True
        return not (self.board.has_valid_move(BLACK) or self.board.has_valid_move(WHITE))
    def handle_pass(self):
        """
        If the current player cannot move but the opponent can, pass the
        turn. Returns True when a pass occurred.
        """
        if not self.board.has_valid_move(self.current_color):
            opponent_color = WHITE if self.current_color == BLACK else BLACK
            if self.board.has_valid_move(opponent_color):
                self.ui.display_pass(self.current_player)
                self.switch_turn()
                return True
        return False
    def play_turn(self):
        """Run a single turn: show state, read a move, apply it."""
        valid_moves = self.board.get_valid_moves(self.current_color)
        self.ui.display_board(self.board, valid_moves)
        self.ui.display_score(self.board, list(self.players.values()))
        self.ui.display_turn(self.current_player, valid_moves)
        move = self.ui.get_move(self.current_player, self.board, valid_moves)
        if move is None:  # user chose to quit
            return False
        row, col = move
        flipped = self.board.place_disc(row, col, self.current_color)
        self.ui.display_move_result(self.current_player, row, col, flipped)
        self.switch_turn()
        return True
    def run(self):
        """Main game loop; runs until the game ends or a player quits."""
        self.ui.display_welcome()
        quit_requested = False
        while not self.is_game_over():
            # Skip a player who has no legal move but whose opponent does.
            if self.handle_pass():
                continue
            if not self.play_turn():
                quit_requested = True
                break
        if not quit_requested:
            self.ui.display_board(self.board)
            self.ui.display_game_over(self.board, list(self.players.values()))
        else:
            self.ui.display_message("Game aborted. Thanks for playing!")