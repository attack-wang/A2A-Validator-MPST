'''
game.py
Defines the Game class, which orchestrates a full Connect Four match:
alternating turns between two players, applying validated moves,
checking for a win or draw after every move, and reporting the result.
'''
import ui
class Game:
    """Turn manager for a two-player Connect Four match."""
    def __init__(self, board, player1, player2):
        """Create a game on `board` with the two participating players."""
        self.board = board
        self.players = (player1, player2)
        self.turn_index = 0
        self.winner = None
        self.winning_line = None
        self.moves_played = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.turn_index]
    def next_turn(self):
        """Hand the turn over to the other player."""
        self.turn_index = 1 - self.turn_index
    def apply_move(self, player, col):
        """Drop `player`'s disc into `col` and increment the move counter.
        Returns the row the disc landed in, or None if the board
        rejected the move (in which case no move is counted).
        """
        row = self.board.drop_disc(col, player.disc)
        if row is not None:
            self.moves_played += 1
        return row
    def is_over(self):
        """Return True when the game has a winner or the board is full."""
        return self.winner is not None or self.board.is_full()
    def play(self):
        """Run the match loop until a player wins or the grid is full."""
        ui.print_message(f"{self.players[0].name} ({self.players[0].disc}) vs "
                         f"{self.players[1].name} ({self.players[1].disc})")
        ui.print_board(self.board)
        while True:
            player = self.current_player
            col = player.get_move(self.board)
            self.apply_move(player, col)
            ui.print_message(f"\n{player.name} placed '{player.disc}' in column {col + 1}.")
            ui.print_board(self.board)
            line = self.board.find_winning_line(player.disc)
            if line:
                self.winner = player
                self.winning_line = line
                ui.print_message(f"\n*** {player.name} ({player.disc}) wins with four in a row! ***")
                ui.print_board(self.board, highlight=line)
                break
            if self.board.is_full():
                ui.print_message("\nThe grid is full — it's a draw!")
                break
            self.next_turn()
        ui.print_message(f"Game over after {self.moves_played} moves.")