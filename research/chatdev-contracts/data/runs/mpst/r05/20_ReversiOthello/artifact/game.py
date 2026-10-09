'''
game.py
Game-flow controller for the Reversi (Othello) game.
The Game class ties together the Board (rules) and the ConsoleUI
(presentation). It manages turn order, handles "pass" situations when a
player has no legal move, detects the end of the game and announces the
final result.
'''
from board import Board, BLACK, WHITE
from ui import ConsoleUI
class Game:
    """Controls one complete Reversi match from start to finish."""
    def __init__(self, ui=None):
        self.board = Board()
        self.ui = ui if ui is not None else ConsoleUI()
        self.current_player = BLACK   # Black always moves first in Othello
        self.game_over = False
    # -- turn management ------------------------------------------------------
    def switch_turn(self):
        """Hand the turn over to the other player."""
        self.current_player = WHITE if self.current_player == BLACK else BLACK
    def is_game_over(self):
        """
        The game ends when the board is full or neither player has a legal
        move.
        """
        return (
            self.board.is_full()
            or (not self.board.has_valid_move(BLACK)
                and not self.board.has_valid_move(WHITE))
        )
    # -- main loop -------------------------------------------------------------
    def run(self):
        """Run the interactive game loop until the match ends or is quit."""
        self.ui.display_welcome()
        while not self.game_over:
            # End the match when the board is full or neither player can move
            if self.is_game_over():
                self.game_over = True
                break
            valid_moves = self.board.get_valid_moves(self.current_player)
            if not valid_moves:
                # Current player cannot move, but the opponent still can: pass
                name = self.ui.player_name(self.current_player)
                self.ui.display_message(f"\n{name} has no legal move and must pass.")
                self.switch_turn()
                continue
            self.ui.display_board(self.board, self.current_player, valid_moves)
            black, white = self.board.count_discs()
            self.ui.display_score(black, white)
            move = self.ui.get_move(self.current_player, valid_moves)
            if move is None:
                self.ui.display_message("\nGame aborted by player. Goodbye!")
                return
            row, col = move
            flipped = self.board.place_disc(row, col, self.current_player)
            self.ui.display_move_result(self.current_player, row, col, len(flipped))
            self.switch_turn()
        # Show the final position and result
        self.ui.display_board(self.board, None, [])
        black, white = self.board.count_discs()
        self.ui.display_final_result(black, white)