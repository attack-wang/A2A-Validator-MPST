'''
game.py
Orchestrates a complete game of Reversi (Othello) between two human
players.
The Game class owns the Board and the two Player objects and glues
them to the GUI.  Its duties are:
    * processing board clicks forwarded by the GUI,
    * validating and applying moves (the Board performs the actual
      rule checks and disc flipping),
    * enforcing turn order, including the "pass" rule when the
      player on turn has no legal move,
    * ending the game when the board is full or neither player can
      move, and announcing the winner,
    * refreshing the board display and the live score after every
      change.
'''
from board import Board
from player import Player
class Game:
    """Turn management and rule orchestration for Reversi."""
    def __init__(self, gui):
        """
        Create a new game bound to `gui`.
        :param gui: Gui object offering bind_game, run, draw_board,
                    update_score, show_message and announce.
        """
        self.board = Board()
        self.gui = gui
        self.players = [
            Player("Player 1", Board.BLACK),
            Player("Player 2", Board.WHITE),
        ]
        self.current_index = 0
        self.game_over = False
        self.gui.bind_game(self)
        self.gui.show_message(
            "Black moves first — click one of the highlighted squares."
        )
        self.refresh()
    # ------------------------------------------------------------------
    # Basic accessors
    # ------------------------------------------------------------------
    @property
    def current_player(self):
        """Return the Player whose turn it is."""
        return self.players[self.current_index]
    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def start(self):
        """Hand control to the GUI event loop."""
        self.gui.run()
    def reset(self):
        """Start a fresh game with the standard starting position."""
        self.board = Board()
        self.current_index = 0
        self.game_over = False
        self.gui.show_message(
            "New game started — Black moves first. Click a highlighted square."
        )
        self.refresh()
    # ------------------------------------------------------------------
    # Move handling
    # ------------------------------------------------------------------
    def handle_click(self, row, col):
        """Process a click on board cell (row, col)."""
        if self.game_over:
            return
        player = self.current_player
        if not self.board.is_valid_move(row, col, player.color):
            self.gui.show_message(
                f"({row + 1}, {col + 1}) is not a legal move for "
                f"{player.name} ({player.color_name}). "
                "Choose one of the highlighted squares."
            )
            return
        flipped = self.board.place_disc(row, col, player.color)
        self.gui.show_message(
            f"{player.name} ({player.color_name}) played "
            f"({row + 1}, {col + 1}) and flipped {len(flipped)} disc(s)."
        )
        self.advance_turn()
    def advance_turn(self):
        """
        Pass play to the other player, applying the pass rule, and
        finish the game when no legal moves remain.
        """
        next_index = 1 - self.current_index
        next_player = self.players[next_index]
        next_moves = self.board.get_valid_moves(next_player.color)
        current_moves = self.board.get_valid_moves(self.current_player.color)
        if self.board.is_full() or (not next_moves and not current_moves):
            self.end_game()
            return
        if next_moves:
            self.current_index = next_index
        else:
            self.gui.show_message(
                f"{next_player.name} ({next_player.color_name}) has no legal "
                f"move and must pass — {self.current_player.name} plays again!"
            )
        self.refresh()
    def end_game(self):
        """Freeze play and announce the final result."""
        self.game_over = True
        black, white = self.board.count_discs()
        self.gui.update_score(black, white, None)
        if black > white:
            result = f"Black wins {black} to {white}!"
        elif white > black:
            result = f"White wins {white} to {black}!"
        else:
            result = f"It's a draw at {black} apiece!"
        self.gui.show_message(f"Game over — final score Black {black} : {white}. {result}")
        self.gui.announce(f"Final score — Black: {black}, White: {white}\n\n{result}")
    # ------------------------------------------------------------------
    # Display refresh
    # ------------------------------------------------------------------
    def refresh(self):
        """Repaint the board and score after any change of state."""
        black, white = self.board.count_discs()
        self.gui.update_score(black, white, self.current_player)
        self.gui.draw_board(
            self.board,
            self.board.get_valid_moves(self.current_player.color),
        )